Dialog = function (body, target, options, cb)
{
  this.body = body || "";
  this.target = target || "";
  this.opts = typeof options !== "undefined" ? options : {};

  // fill in missing options
  if (!this.opts.w)
    this.opts.w = 400;
  if (!this.opts.h)
    this.opts.h = 400;
  if (typeof this.opts.t === "undefined")
    this.opts.t = 100; // Math.floor(200 * Math.random());
  if (typeof this.opts.l === "undefined")
    this.opts.l = 150; // Math.floor(200 * Math.random());
  if (!this.opts.parent)
    this.opts.parent = window;
  if (!this.opts.parent.openedFolders)
    this.opts.parent.openedFolders = {};
  if (!this.opts.title)
    this.opts.title = "";
  if (!this.opts.fit)
    this.opts.fit = false;
  if (!this.opts.multi)
    this.opts.multi = false;

  // check if I should open
  if (this.opts.parent.openedFolders[target] && !this.opts.multi)
    return;
  this.opts.parent.openedFolders[target] = true;

  this.id = Math.floor(20000 * Math.random());
  this.el = document.createElement('div');
  this.el.className = "popup-wrap floating";
  this.el.style.width = this.opts.w + "px";
  this.el.style.height = this.opts.h + "px";
  this.el.style.top = this.opts.t + "px";
  this.el.style.left = this.opts.l + "px";


  var handle = document.createElement('div');
  handle.className = "popup-handle popup-draggable";
  var handleCentre = document.createElement('div');
  handleCentre.className = "popup-handle popup-centre";

  var mid = document.createElement('div');
  mid.className = "popup-mid";

  // action buttons
  var actions = document.createElement('div');
  actions.className = "popup-actions";
  var close = document.createElement('div');
  close.innerHTML = "&#10005;";
  close.className = "popup-close";
  var self = this;
  actions.onclick = function () {
    self.close();
  };

  var title = document.createElement('div');
  title.className = "popup-title";
  title.innerText = this.opts.title;
  var content = document.createElement('div');
  content.className = "popup-content";
  // content.innerHTML = this.body;
  actions.appendChild(close);
  handle.appendChild(actions);
  handleCentre.appendChild(title);
  mid.appendChild(content);

  // structure
  handle.appendChild(handleCentre);
  this.el.appendChild(handle);
  this.el.appendChild(mid);

  this.el.id = this.id;

  this.opts.parent.document.body.appendChild(this.el);

  this.popupise();
  this.focus();
  // this.closed = false;
  if (cb) {
    cb(content);
  }
};

Dialog.prototype.popupise = function ()
{
  var self = this;
  self.opts.parent.jQuery(self.el)
          // .resizable({
          //   minHeight: 150,
          //   minWidth: 150,
          //   start: function (event, ui) {
          //     self.opts.parent.jQuery(".popup-iframe-cover").css('z-index', 3000);
          //   },
          //   stop: function (event, ui) {
          //     self.opts.parent.jQuery(".popup-iframe-cover").css('z-index', -1);
          //   }
          // })
          .draggable({
            // iframeFix: true,
            handle: "div.popup-draggable",
            stack: ".floating"
          })
          .bind("click", function (e) {
            // since we contain an iframe, this is actually bound only to
            // the toolbar
            var largestZ = 1000;
            self.opts.parent.jQuery(".floating").each(function (i) {
              var currentZ = parseFloat(self.opts.parent.jQuery(this).css("zIndex"));
              largestZ = currentZ > largestZ ? currentZ : largestZ;
            });
            self.opts.parent.jQuery(self.el).css("zIndex", largestZ + 1);
          });
  // self.opts.parent.jQuery( ".popup-handle" ).disableSelection(); // better use css
};

Dialog.prototype.focus = function ()
{
  return this.el.focus();
};

Dialog.prototype.close = function ()
{
  this.closed = true;
  this.opts.parent.openedFolders[this.target] = false;
  this.opts.parent.jQuery(this.el).remove();
};
