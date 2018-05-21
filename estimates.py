# -*- coding: utf-8 -*-
"""
Security cross-estimation for lattice based schemes proposed to NIST against the primal and dual attacks.
This script assumes that the LWE estimator commit 9302d42 is present in a subdirectory `estimator`.

NOTATION:

    LWE
    n       lwe secret dimension
    k       mlwe rank
    q       lwe modulo
    sd      lwe error standard deviation (if secret is normal form, also the secret standard devation)
    m       number of lwe samples

AUTHOR:

    Rachel Player - 2017, 2018
    Fernando Virdia - 2017, 2018
    Thomas Wunderer - 2018

"""


from sage.all import *
import estimator as est
from schemes import LWE_SCHEMES, NTRU_SCHEMES
from cost_asymptotics import BKZ_COST_ASYMPTOTICS
from html import generate_json
from inspect import getsource
try:
    from config import NCPUS
except ImportError:
    NCPUS = 2
try:
    from config import SOBJPATH
except ImportError:
    SOBJPATH = "all_the_schemes.sobj"


def flatten(l):
    """ Flattens a list of lists into a list containing the elements of each
        sublist.

    :params l:      list of lists

    :return:        flattened list
    """
    return [item for sublist in l for item in sublist]


@parallel(ncpus=NCPUS)
def para_cost_scheme(scheme):
    """ Utility function for running LWE costing in parallel.

    :param scheme:      list containing an LWE scheme object
    """
    return cost_scheme(scheme[0], dual_use_lll=True) # false worsens it


def cost_scheme(scheme, debug=False, dual_use_lll=True):
    """ Costs LWE scheme by calling the [APS15] estimator.
        Costing is done against primal and dual attacks, and considers the distribution
        of the secret vector to apply scaling and dropping of columns.

        :params scheme:         LWE scheme object
        :params debug:          Boolean value, if set to True, catched exceptions are re-raised.

        :returns estimates:     list of estimated costs for the primal and dual attack
    """
    sname = scheme["name"]
    params = scheme["params"]

    # verbose output
    print "Costing lwe scheme: %s"%(sname)

    # loop parametrisations
    estimates = []
    for instance in params:
        instance_estimates = {"primal": [], "dual": []}
        if type(instance) != list:
            # always consider param objects as part of a list
            instance = [instance]
        for param in instance:
            # cast everything to python type so we can json.dump it
            n = param["n"]
            sd = param["sd"]
            q = param["q"]
            secret_distribution = param["secret_distribution"]
            # NOTE: code for arbitrary distributions, feature not available in the estimator yet
            # if type(secret_distribution) == dict and "mean" not in secret_distribution:
            #     sec_dist = {}
            #     sec_dist = {
            #         "is_sparse": est.SDis.is_sparse(secret_distribution),
            #         "is_small": est.SDis.is_small(secret_distribution),
            #         "bounds": est.SDis.bounds(secret_distribution),
            #         "is_bounded_uniform": est.SDis.is_bounded_uniform(secret_distribution),
            #         "is_ternary": est.SDis.is_ternary(secret_distribution),
            #         "nonzero": floor(est.SDis.nonzero(secret_distribution, n)),
            #         "mean": est.SDis.mean(secret_distribution),
            #         "variance": est.SDis.variance(secret_distribution),
            #     }
            #     secret_distribution = sec_dist
            alpha = sqrt(2*pi) * sd / RR(q)
            primal_estimate_cost = {}
            dual_estimate_cost = {}

            is_ntru = "NTRU" in scheme["assumption"]
            samples = [n] if is_ntru else [n, 2*n]

            try:
                # loop cost models
                for cost_model in BKZ_COST_ASYMPTOTICS:
                    cname = cost_model["name"]
                    reduction_cost_model = cost_model["reduction_cost_model"]
                    success_probability = cost_model["success_probability"]
                    primal_results = {"n": {}, "2n": {}}
                    if not is_ntru:
                        dual_results = {"n": {}, "2n": {}}

                    for m in samples:
                        dropped = False
                        # Estimate standard attacks. The estimator will apply any possible scaling
                        cost_primal = est.primal_usvp(n, alpha, q, secret_distribution=secret_distribution,
                                                        m=m,  success_probability=success_probability,
                                                        reduction_cost_model=reduction_cost_model)
                        if not is_ntru:
                            cost_dual = est.dual_scale(n, alpha, q, secret_distribution=secret_distribution,
                                                            m=m, success_probability=success_probability,
                                                            reduction_cost_model=reduction_cost_model, use_lll=dual_use_lll)

                        if est.SDis.is_bounded_uniform(secret_distribution) or type(secret_distribution) == dict:
                            a, b = est.SDis.bounds(secret_distribution)
                            if -a == b:
                                # Try guessing secret entries via drop_and_solve
                                primald = est.partial(est.drop_and_solve, est.primal_usvp, postprocess=False, decision=False)
                                cost_primal_dropped = primald(n, alpha, q, secret_distribution=secret_distribution,
                                                        m=m,  success_probability=success_probability,
                                                        reduction_cost_model=reduction_cost_model, rotations=is_ntru)
                                if not is_ntru:
                                    duald = est.partial(est.drop_and_solve, est.dual_scale, postprocess=True)
                                    cost_dual_dropped = duald(n, alpha, q, secret_distribution=secret_distribution,
                                                            m=m,  success_probability=success_probability,
                                                            reduction_cost_model=reduction_cost_model, use_lll=dual_use_lll)

                                # Sometimes drop_and_solve results in a more costly attack
                                if cost_primal_dropped["rop"] < cost_primal["rop"]:
                                    cost_primal = cost_primal_dropped
                                    dropped = True
                                if not is_ntru:
                                    if cost_dual_dropped["rop"] < cost_dual["rop"]:
                                        cost_dual = cost_dual_dropped
                                        dropped = True

                        # save results
                        primal_results["n" if m == n else "2n"] = {
                            "name": cname,
                            "dim":  int(cost_primal["d"]),
                            "beta": int(cost_primal["beta"]),
                            "rop":  int(ceil(log(cost_primal["rop"], 2))),
                            "drop": dropped,
                            "inst": instance.index(param),
                        }
                        if not is_ntru:
                            dual_results["n" if m == n else "2n"] = {
                                "name": cname,
                                "dim": int(cost_dual["d"]),
                                "beta": int(cost_dual["beta"]),
                                "rop": int(ceil(log(cost_dual["rop"], 2))),
                                "drop": dropped,
                                "inst": instance.index(param),
                            }

                    primal_estimate_cost[cname] = primal_results
                    if not is_ntru:
                        dual_estimate_cost[cname] = dual_results

            except Exception, e:
                primal_estimate_cost["error"] = str(e)
                if not is_ntru:
                    dual_estimate_cost["error"] = str(e)
                if debug:
                    raise

            instance_estimates["primal"] += [primal_estimate_cost]
            if not is_ntru:
                instance_estimates["dual"] += [dual_estimate_cost]

        # there may be complexity swaps for an instance based on multiple problems
        # here we choose the cheapest problem always
        
        # TODO: for each attack choose the cheapest cost
        cheapest_parameters = {}
        for atk in instance_estimates:
            cheapest_parameters[atk] = {}
            for cost_model in BKZ_COST_ASYMPTOTICS:
                cname = cost_model["name"]
                cheapest_parameters[atk][cname] = {}
                for m in ["n"] if is_ntru else ["n", "2n"]:
                    cheapest_parameters[atk][cname][m] = { "rop": infinity }
                    for inst_est in instance_estimates[atk]:
                        # pick the cheapest attack based on the instance's parameters
                        if inst_est[cname][m]["rop"] < cheapest_parameters[atk][cname][m]["rop"]:
                            cheapest_parameters[atk][cname][m] = inst_est[cname][m]

        # prepare json data structure
        # NOTE: for the uuid of an instance we just look at the first parameter set
        n = instance[0]["n"]
        sd = instance[0]["sd"]
        q = instance[0]["q"]
        key = "%s-%04d-%.2f-%d"%(sname,n,sd,q)
        primal_estimate = {
            "attack": "primal",
            "key": key,
            "scheme": {
                "name": sname,
                "primitive": scheme["primitive"],
                "assumption": scheme["assumption"],
            },
            "param": instance,
            "cost": cheapest_parameters["primal"],
        }

        if not is_ntru:
            dual_estimate = {
                "attack": "dual",
                "key": key,
                "scheme": {
                    "name": sname,
                    "primitive": scheme["primitive"],
                    "assumption": scheme["assumption"],
                },
                "param": instance,
                "cost": cheapest_parameters["dual"],
            }

        estimates += [primal_estimate]
        if not is_ntru:
            estimates += [dual_estimate]
        
    return estimates


def main():
    """ Main function costing LWE and NTRU schemes.
        Runs each scheme costing in parallel.
        Results are saved as a Sage object and as an HTML table.

    :return estimates_list:     list containing scheme costs
    """

    lwe_estimates = list(para_cost_scheme([[s] for s in LWE_SCHEMES + NTRU_SCHEMES]))
    estimates_list = flatten([x[1] for x in lwe_estimates])

    # save estimates as sage object
    save(estimates_list, SOBJPATH)

    try:
        print "Generating html"
        generate_json(estimates_list)

    except Exception, e:
        print "Error generating html:", e

    print "Done."
    return estimates_list


def debug_call():
    """ Debug call to a single costing.
        It avoids the automatic exception handling done by @parallel.

    """
    return cost_scheme(LWE_SCHEMES[0], debug=True)


""" Run main is executed as a script.
    Don't if attached/loaded/imported into sage/python.
"""
import __main__
if __name__ == "__main__" and hasattr(__main__, '__file__'):
    main()
    # debug_call()
