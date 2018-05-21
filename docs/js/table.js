if (!String.prototype.format) {
  String.prototype.format = function() {
    var args = arguments;
    return this.replace(/{(\d+)}/g, function(match, number) {
      return typeof args[number] != 'undefined'
        ? args[number]
        : match
      ;
    });
  };
}

var tables = {};

var drawTable = function (tableid, m, cb) {
  // draw the head
  var thead0 = $(tableid + " > thead > tr")[0];
  var hscheme = document.createElement("th");
  hscheme.innerText = "Scheme";
  hscheme.rowSpan = 2;
  $(hscheme).data("select", "1");
  thead0.appendChild(hscheme);
  var hassumption = document.createElement("th");
  hassumption.innerText = "Assumption";
  hassumption.rowSpan = 2;
  $(hassumption).data("select", "1");
  thead0.appendChild(hassumption);
  var hprimitive = document.createElement("th");
  hprimitive.innerText = "Primitive";
  hprimitive.rowSpan = 2;
  $(hprimitive).data("select", "1");
  thead0.appendChild(hprimitive);
  var hparameters = document.createElement("th");
  hparameters.innerText = "Parameters";
  hparameters.rowSpan = 2;
  thead0.appendChild(hparameters);
  var hclaimed = document.createElement("th");
  hclaimed.innerText = "Claimed security";
  hclaimed.rowSpan = 2;
  thead0.appendChild(hclaimed);
  var hcategory = document.createElement("th");
  hcategory.innerText = "NIST Category";
  hcategory.rowSpan = 2;
  $(hcategory).data("select", "1");
  thead0.appendChild(hcategory);
  var hatk = document.createElement("th");
  hatk.innerText = "Attack";
  hatk.rowSpan = 2;
  $(hatk).data("select", "1");
  thead0.appendChild(hatk);
  var hmodels = document.createElement("th");
  hmodels.innerText = "Proposed BKZ cost models";
  hmodels.colSpan = models.length;
  thead0.appendChild(hmodels);

  var thead1 = $(tableid + " > thead > tr")[1];
  for (var j = 0; j < models.length; j++) {
    var th = document.createElement("th");
    th.innerText = models[j].name;
    thead1.appendChild(th);
  }

  // draw the body
  var tbody = $(tableid + " > tbody")[0];
  console.log("estimates.length = " + estimates.length);
  for (var i = 0; i < estimates.length; i++) {
    var attack = estimates[i];

    // only parse estimates for this table

    if ((attack.scheme.assumption[0] === "NTRU" && m !== "ntru")
        || (attack.scheme.assumption[0] !== "NTRU" && m === "ntru")) {
      continue;
    }

    var tr = document.createElement("tr");
    var scheme = document.createElement("td");
    scheme.innerText = attack.scheme.name;
    tr.appendChild(scheme);
    var assumption = document.createElement("td");
    assumption.className = "ra";
    assumption.innerText = attack.scheme.assumption.join(", ");
    tr.appendChild(assumption);
    var primitive = document.createElement("td");
    primitive.className = "ra";
    primitive.innerText = attack.scheme.primitive.join(", ");
    tr.appendChild(primitive);
    var parameters = document.createElement("td");
    parameters.className = "cell-overflow";
    var subparams = document.createElement("div");
    subparams.className = "cell-overflow";
    
    for (var j = 0; j < attack.param.length; j++) {
      console.log(attack.param[j]);
      if (m === "ntru") {
        subparams.innerHTML += "n = {0}, q = {1}, ⌈log<sub>2</sub> q⌉ = {2},<br>‖f‖<sub>2</sub> = {3}, ‖g‖<sub>2</sub> = {4}".format(
          attack.param[j].n,
          attack.param[j].q,
          Math.ceil(Math.log2(attack.param[j].q)),
          attack.param[j].norm_f.toFixed(2),
          attack.param[j].norm_g.toFixed(2)
        );
      } else {
        subparams.innerHTML += "n = {0}, ".format(
          attack.param[j].n
        );
        if ("k" in attack.param[j]) {
          subparams.innerHTML += "k = {0}, ".format(
            attack.param[j].k
          );
        }
        subparams.innerHTML += "q = {0}, ⌈log<sub>2</sub> q⌉ = {1},<br>σ = {2}, secret = {3}".format(
          attack.param[j].q,
          Math.ceil(Math.log2(attack.param[j].q)),
          attack.param[j].sd.toFixed(2),
          attack.param[j].secret_distribution
        );
      }
      if ("ring" in attack.param[j]) {
        var ring = attack.param[j].ring;
        // ring = ring.replace("\\ZZ_q", "ℤ<sub>q</sub>");
        ring = ring.replace("\\sum_{i=0}^n", "∑<span class='supsub'><sup class='sup'>n</sup><sub class='sub'>i = 0</sub></span>");
        ring = ring.replace("\\sum^n_{i=0}", "∑<span class='supsub'><sup class='sup'>n</sup><sub class='sub'>i = 0</sub></span>");
        ring = ring.replace("\\sum_{i=0}^{n-1}", "∑<span class='supsub'><sup class='sup'>n-1</sup><sub class='sub'>i = 0</sub></span>");
        ring = ring.replace("\\sum^{n-1}_{i=0}", "∑<span class='supsub'><sup class='sup'>n-1</sup><sub class='sub'>i = 0</sub></span>");
        ring = ring.replace("\\sum_{i=1}^{n-1}", "∑<span class='supsub'><sup class='sup'>n-1</sup><sub class='sub'>i = 1</sub></span>");
        ring = ring.replace("\\sum^{n-1}_{i=1}", "∑<span class='supsub'><sup class='sup'>n-1</sup><sub class='sub'>i = 1</sub></span>");
        ring = ring.replace("^n", "<sup>n</sup>");
        ring = ring.replace("^p", "<sup>p</sup>");
        ring = ring.replace("^{n/k}", "<sup>n/k</sup>");
        ring = ring.replace("^{n/(2k)}", "<sup>n/(2k)</sup>");
        ring = ring.replace("^i", "<sup>i</sup>");
        ring = ring.replace("_i", "<sub>i</sub>");
        ring = ring.replace("_0", "<sub>0</sub>");
        ring = ring.replace("\\text{ *}", "");
        ring = ring.replace("\\text{ \\textdagger}", "");
        subparams.innerHTML += ",<br>𝜙 = {0}".format(ring);
      }
      if (j < attack.param.length - 1) {
        subparams.innerHTML += '<br><div class="par-sep"></div>';
      }
    }
    parameters.appendChild(subparams);
    tr.appendChild(parameters);
    var claimed = document.createElement("td");
    claimed.className = "ra";
    // NOTE: we pick as claim the lowest taken across parameters for the single instance
    _claim = 9999;
    for (var j = 0; j < attack.param.length; j++) {
      _claim = Math.min(_claim, attack.param[j].claimed);
    }
    claimed.innerText = _claim;
    tr.appendChild(claimed);
    var category = document.createElement("td");
    category.className = "ra";
    // NOTE: we assume an instance with multiple parameter sets
    // will have them all aim at the same category
    category.innerText = attack.param[0].category.join(", ");
    tr.appendChild(category);
    var atk = document.createElement("td");
    atk.className = "ra";
    atk.innerText = attack.attack;
    tr.appendChild(atk);

    for (var j = 0; j < models.length; j++) {
      var cell = document.createElement("td");
      if (models[j].name in attack.cost) {
        var cost = m === "ntru" ? (
          "n" in attack.cost[models[j].name] ? attack.cost[models[j].name]["n"] : attack.cost[models[j].name]
        ) : attack.cost[models[j].name][m];
        var cell = document.createElement("td");
        cell.className = "data-entry";
        cell.innerText = cost.rop;
        var inst = cost.inst;

        // add reproducible result
        var content = "# To reproduce the estimate run this snippet on http://aleph.sagemath.org/\n";
        content += "# Ring ops: {0}\n".format(cost.rop);
        content += "# Block size: {0}\n".format(cost.beta);
        content += "# Dimension: {0}\n".format(cost.dim);
        if (attack.param.length > 1) {
          content += "# NOTE: This scheme relies on different hard problem instances for key recovery and message recovery.\nThe code below gives the cost of the cheaper of the two attacks under the chosen cost model.\n"
        }
        content += "load('https://bitbucket.org/malb/lwe-estimator/raw/HEAD/estimator.py')\n";
        content += "n = {0}\n".format(attack.param[inst].n);
        // if ("k" in attack.param) {
        //   content += "k = {0}\n".format(attack.param.k);
        // }
        content += "sd = {0}\n".format(attack.param[inst].sd);
        content += "q = {0}\n".format(attack.param[inst].q);
        content += "alpha = sqrt(2*pi)*sd/RR(q)\n";
        // content += "m = {0}\n".format(m == "2n"? "2*n/k" : "n/k");
        content += "m = {0}\n".format(m == "2n"? "2*n" : "n");
        content += "secret_distribution = {0}\n".format(attack.param[inst].secret_distribution == "normal" ? '"normal"' : attack.param[inst].secret_distribution);
        content += "success_probability = 0.99\n";
        content += "reduction_cost_model = {0}\n".format(models[j].lambda);

        if (attack.attack === "primal" && cost.drop == false) {
          content += "primal_usvp(n, alpha, q, secret_distribution=secret_distribution, m=m, ";
          content += "success_probability=success_probability, reduction_cost_model=reduction_cost_model)";
        } else if (attack.attack === "primal" && cost.drop == true) {
          content += "primald = partial(drop_and_solve, primal_usvp, postprocess=False, decision=False)\n";
          content += "primald(n, alpha, q, secret_distribution=secret_distribution, ";
          content += "m=m,  success_probability=success_probability, reduction_cost_model=reduction_cost_model";
          content += m === "ntru" ? ", rotations=True)" : ")";
        } else if (attack.attack === "dual" && cost.drop == false) {
          content += "dual_scale(n, alpha, q, secret_distribution=secret_distribution, ";
          content += "m=m, success_probability=success_probability, reduction_cost_model=reduction_cost_model)";
        } else if (attack.attack === "dual" && cost.drop == true) {
          content += "duald = partial(drop_and_solve, dual_scale, postprocess=True)\n";
          content += "duald(n, alpha, q, secret_distribution=secret_distribution, ";
          content += "m=m, success_probability=success_probability, reduction_cost_model=reduction_cost_model)";
        }
        cell.pqcContent = content;
        cell.pqcTitle = "{0} – {1}".format(attack.scheme.name, cost.name);
        cell.onclick = function (ev) {
          var self = this;
          new Dialog(self.pqcContent, "0", {
            t: ev.pageY - 10,
            l: ev.pageX - 100,
            h: 350,
            w: 620,
            title: self.pqcTitle,
            multi: true
          }, function (content) {
            self.myCodeMirror = CodeMirror(content, {
              value: self.pqcContent,
              mode: "python",
              readOnly: true,
              lineWrapping: true,
              lineNumbers: true,
              theme: "mdn-like"
              // theme: "neo"
            });
          });
        };
      }
      tr.appendChild(cell);
    }
    tbody.appendChild(tr);
  }

  // enable sortable table
  var tab = $(tableid).DataTable({
    order: [[0, "asc"]],
    scrollY: "calc(100vh - 420px)",
    scrollX: true,
    scrollCollapse: true,
    paging: false,
    initComplete: function () {
      this.api().columns().every( function () {
        var column = this;
        if ($(column.header()).data("select") == 1) {
          var select = $('<select><option value=""></option></select>')
          .appendTo( $(column.header()) )
          .on( 'change', function () {
            var val = $.fn.dataTable.util.escapeRegex($(this).val().trim());
            column.search( val ? '(^|.*[ ])('+val+'($|,)).*$' : '', true, false)
            .draw();
          });
          select.on('click', function (ev) {
            ev.stopImmediatePropagation();
          });
          filters = []
          column.data().unique().sort().each(function (d, j) {
            var dd = d.split(',');
            for (i in dd) {
              var en = dd[i].trim();
              if (filters.indexOf(en) < 0) {
                filters.push(en);
                select.append('<option value="'+en+'">'+en+'</option>');
              }
            }
          });
        }
      });
    }
  });
  tables[tableid.substr(1)] = tab;

  // callback
  if (cb) {
    cb();
  }
};

var drawColSel = function (cb) {
  var sel = document.getElementById("select-cols-wrap").children[0];
  var groups = {};

  // load models
  for (var i = 0; i < models.length; i++) {
    // add group if necessary
    if (!(models[i].group in groups)) {
      var grp = document.createElement("optgroup");
      grp.label = models[i].group;
      groups[models[i].group] = grp;
    }
    var opt = document.createElement("option");
    opt.value = models[i].name;
    opt.innerText = models[i].name;
    opt.selected = true;
    groups[models[i].group].appendChild(opt);
  }
  for (var i = 0; i < Object.keys(groups).length; i++) {
    sel.appendChild(groups[Object.keys(groups)[i]]);
  }
  if (cb) {
    cb();
  }
}

var filterCols = function () {
  // loop opts looking for selected ones
  var counter = 6; // skip first few columns, go to cost models
  var sel = document.getElementById("select-cols-wrap").children[0];
  for (var i = 0; i < sel.children.length; i++) {
    var grp = sel.children[i];
    for (var j = 0; j < grp.children.length; j++) {
      var opt = grp.children[j];
      counter++;
      var id = $(".dataTables_wrapper:visible")[0].id.split("_")[0];
      tables[id].column(counter).visible(opt.selected);
    }
  }
};

$(document).ready(function () {
  // enable radio buttons
  $("input[name='radio-m']").checkboxradio().change(function (ev) {
    tableid = $("input[name='radio-m']:checked").val();
    $("#lwe-n_wrapper").hide();
    $("#lwe-2n_wrapper").hide();
    $("#ntru_wrapper").hide();
    $(tableid+"_wrapper").show();
    // adjust column widths
    var id = $(".dataTables_wrapper:visible")[0]
    if (id) {
      id = id.id.split("_")[0];
      tables[id].columns.adjust();
    }
    filterCols();
  });

  // render the tables
  drawTable("#lwe-n", "n", function () {
    drawTable("#lwe-2n", "2n", function () {
      drawTable("#ntru", "ntru", function () {
        // select lwe-n after giving a chance for everything to render
        $("#radio-n").click();
        $("#spinner").hide();
        $("#tables").show();
        var id = $(".dataTables_wrapper:visible")[0].id.split("_")[0];
        tables[id].columns.adjust();
      });
    });
  });

  // draw column select
  drawColSel(function () {
    $('select[multiple]').multiselect({
      columns: 2,
      search: false,
      selectAll: true,
      selectGroup: true,
      texts: {
          placeholder: 'Select cost models',
      },
      onOptionClick: filterCols,
      onSelectAll: filterCols
    });
  })

  // parameters and cost tooltips
  $( document ).tooltip({
    items: "td.cell-overflow, th",
    track: true,
    content: function () {
      var el = $(this);
      if (el[0].localName == "th") {
        for (var i = 0; i < models.length; i++) {
          if (models[i].name === el.text()) {
            return models[i].human;
          }
        }
      } else {
        return el.children(":first").html();
      }
    },
    show: {
      effect: "fadeIn",
      delay: 0,
      duration: 0
    },
    hide: {
      effect: "fadeOut",
      delay: 0,
      duration: 0
    }
  });
 });
