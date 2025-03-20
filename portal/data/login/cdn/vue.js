/*!
 * Vue.js v2.7.16
 * (c) 2014-2023 Evan You
 * Released under the MIT License.
 */
(function (global, factory) {
  typeof exports === 'object' && typeof module !== 'undefined' ? module.exports = factory() :
  typeof define === 'function' && define.amd ? define(factory) :
  (global = typeof globalThis !== 'undefined' ? globalThis : global || self, global.Vue = factory());
})(this, (function () { 'use strict';

  var emptyObject = Object.freeze({});
  var isArray = Array.isArray;
  // These helpers produce better VM code in JS engines due to their
  // explicitness and function inlining.
  function isUndef(v) {
      return v === undefined || v === null;
  }
  function isDef(v) {
      return v !== undefined && v !== null;
  }
  function isTrue(v) {
      return v === true;
  }
  function isFalse(v) {
      return v === false;
  }
  /**
   * Check if value is primitive.
   */
  function isPrimitive(value) {
      return (typeof value === 'string' ||
          typeof value === 'number' ||
          // $flow-disable-line
          typeof value === 'symbol' ||
          typeof value === 'boolean');
  }
  function isFunction(value) {
      return typeof value === 'function';
  }
  /**
   * Quick object check - this is primarily used to tell
   * objects from primitive values when we know the value
   * is a JSON-compliant type.
   */
  function isObject(obj) {
      return obj !== null && typeof obj === 'object';
  }
  /**
   * Get the raw type string of a value, e.g., [object Object].
   */
  var _toString = Object.prototype.toString;
  function toRawType(value) {
      return _toString.call(value).slice(8, -1);
  }
  /**
   * Strict object type check. Only returns true
   * for plain JavaScript objects.
   */
  function isPlainObject(obj) {
      return _toString.call(obj) === '[object Object]';
  }
  function isRegExp(v) {
      return _toString.call(v) === '[object RegExp]';
  }
  /**
   * Check if val is a valid array index.
   */
  function isValidArrayIndex(val) {
      var n = parseFloat(String(val));
      return n >= 0 && Math.floor(n) === n && isFinite(val);
  }
  function isPromise(val) {
      return (isDef(val) &&
          typeof val.then === 'function' &&
          typeof val.catch === 'function');
  }
  /**
   * Convert a value to a string that is actually rendered.
   */
  function toString(val) {
      return val == null
          ? ''
          : Array.isArray(val) || (isPlainObject(val) && val.toString === _toString)
              ? JSON.stringify(val, replacer, 2)
              : String(val);
  }
  function replacer(_key, val) {
      // avoid circular deps from v3
      if (val && val.__v_isRef) {
          return val.value;
      }
      return val;
  }
  /**
   * Convert an input value to a number for persistence.
   * If the conversion fails, return original string.
   */
  function toNumber(val) {
      var n = parseFloat(val);
      return isNaN(n) ? val : n;
  }
  /**
   * Make a map and return a function for checking if a key
   * is in that map.
   */
  function makeMap(str, expectsLowerCase) {
      var map = Object.create(null);
      var list = str.split(',');
      for (var i = 0; i < list.length; i++) {
          map[list[i]] = true;
      }
      return expectsLowerCase ? function (val) { return map[val.toLowerCase()]; } : function (val) { return map[val]; };
  }
  /**
   * Check if a tag is a built-in tag.
   */
  var isBuiltInTag = makeMap('slot,component', true);
  /**
   * Check if an attribute is a reserved attribute.
   */
  var isReservedAttribute = makeMap('key,ref,slot,slot-scope,is');
  /**
   * Remove an item from an array.
   */
  function remove$2(arr, item) {
      var len = arr.length;
      if (len) {
          // fast path for the only / last item
          if (item === arr[len - 1]) {
              arr.length = len - 1;
              return;
          }
          var index = arr.indexOf(item);
          if (index > -1) {
              return arr.splice(index, 1);
          }
      }
  }
  /**
   * Check whether an object has the property.
   */
  var hasOwnProperty = Object.prototype.hasOwnProperty;
  function hasOwn(obj, key) {
      return hasOwnProperty.call(obj, key);
  }
  /**
   * Create a cached version of a pure function.
   */
  function cached(fn) {
      var cache = Object.create(null);
      return function cachedFn(str) {
          var hit = cache[str];
          return hit || (cache[str] = fn(str));
      };
  }
  /**
   * Camelize a hyphen-delimited string.
   */
  var camelizeRE = /-(\w)/g;
  var camelize = cached(function (str) {
      return str.replace(camelizeRE, function (_, c) { return (c ? c.toUpperCase() : ''); });
  });
  /**
   * Capitalize a string.
   */
  var capitalize = cached(function (str) {
      return str.charAt(0).toUpperCase() + str.slice(1);
  });
  /**
   * Hyphenate a camelCase string.
   */
  var hyphenateRE = /\B([A-Z])/g;
  var hyphenate = cached(function (str) {
      return str.replace(hyphenateRE, '-$1').toLowerCase();
  });
  /**
   * Simple bind polyfill for environments that do not support it,
   * e.g., PhantomJS 1.x. Technically, we don't need this anymore
   * since native bind is now performant enough in most browsers.
   * But removing it would mean breaking code that was able to run in
   * PhantomJS 1.x, so this must be kept for backward compatibility.
   */
  /* istanbul ignore next */
  function polyfillBind(fn, ctx) {
      function boundFn(a) {
          var l = arguments.length;
          return l
              ? l > 1
                  ? fn.apply(ctx, arguments)
                  : fn.call(ctx, a)
              : fn.call(ctx);
      }
      boundFn._length = fn.length;
      return boundFn;
  }
  function nativeBind(fn, ctx) {
      return fn.bind(ctx);
  }
  // @ts-expect-error bind cannot be `undefined`
  var bind$1 = Function.prototype.bind ? nativeBind : polyfillBind;
  /**
   * Convert an Array-like object to a real Array.
   */
  function toArray(list, start) {
      start = start || 0;
      var i = list.length - start;
      var ret = new Array(i);
      while (i--) {
          ret[i] = list[i + start];
      }
      return ret;
  }
  /**
   * Mix properties into target object.
   */
  function extend(to, _from) {
      for (var key in _from) {
          to[key] = _from[key];
      }
      return to;
  }
  /**
   * Merge an Array of Objects into a single Object.
   */
  function toObject(arr) {
      var res = {};
      for (var i = 0; i < arr.length; i++) {
          if (arr[i]) {
              extend(res, arr[i]);
          }
      }
      return res;
  }
  /* eslint-disable no-unused-vars */
  /**
   * Perform no operation.
   * Stubbing args to make Flow happy without leaving useless transpiled code
   * with ...rest (https://flow.org/blog/2017/05/07/Strict-Function-Call-Arity/).
   */
  function noop(a, b, c) { }
  /**
   * Always return false.
   */
  var no = function (a, b, c) { return false; };
  /* eslint-enable no-unused-vars */
  /**
   * Return the same value.
   */
  var identity = function (_) { return _; };
  /**
   * Generate a string containing static keys from compiler modules.
   */
  function genStaticKeys$1(modules) {
      return modules
          .reduce(function (keys, m) { return keys.concat(m.staticKeys || []); }, [])
          .join(',');
  }
  /**
   * Check if two values are loosely equal - that is,
   * if they are plain objects, do they have the same shape?
   */
  function looseEqual(a, b) {
      if (a === b)
          return true;
      var isObjectA = isObject(a);
      var isObjectB = isObject(b);
      if (isObjectA && isObjectB) {
          try {
              var isArrayA = Array.isArray(a);
              var isArrayB = Array.isArray(b);
              if (isArrayA && isArrayB) {
                  return (a.length === b.length &&
                      a.every(function (e, i) {
                          return looseEqual(e, b[i]);
                      }));
              }
              else if (a instanceof Date && b instanceof Date) {
                  return a.getTime() === b.getTime();
              }
              else if (!isArrayA && !isArrayB) {
                  var keysA = Object.keys(a);
                  var keysB = Object.keys(b);
                  return (keysA.length === keysB.length &&
                      keysA.every(function (key) {
                          return looseEqual(a[key], b[key]);
                      }));
              }
              else {
                  /* istanbul ignore next */
                  return false;
              }
          }
          catch (e) {
              /* istanbul ignore next */
              return false;
          }
      }
      else if (!isObjectA && !isObjectB) {
          return String(a) === String(b);
      }
      else {
          return false;
      }
  }
  /**
   * Return the first index at which a loosely equal value can be
   * found in the array (if value is a plain object, the array must
   * contain an object of the same shape), or -1 if it is not present.
   */
  function looseIndexOf(arr, val) {
      for (var i = 0; i < arr.length; i++) {
          if (looseEqual(arr[i], val))
              return i;
      }
      return -1;
  }
  /**
   * Ensure a function is called only once.
   */
  function once(fn) {
      var called = false;
      return function () {
          if (!called) {
              called = true;
              fn.apply(this, arguments);
          }
      };
  }
  // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/is#polyfill
  function hasChanged(x, y) {
      if (x === y) {
          return x === 0 && 1 / x !== 1 / y;
      }
      else {
          return x === x || y === y;
      }
  }

  var SSR_ATTR = 'data-server-rendered';
  var ASSET_TYPES = ['component', 'directive', 'filter'];
  var LIFECYCLE_HOOKS = [
      'beforeCreate',
      'created',
      'beforeMount',
      'mounted',
      'beforeUpdate',
      'updated',
      'beforeDestroy',
      'destroyed',
      'activated',
      'deactivated',
      'errorCaptured',
      'serverPrefetch',
      'renderTracked',
      'renderTriggered'
  ];

  var config = {
      /**
       * Option merge strategies (used in core/util/options)
       */
      // $flow-disable-line
      optionMergeStrategies: Object.create(null),
      /**
       * Whether to suppress warnings.
       */
      silent: false,
      /**
       * Show production mode tip message on boot?
       */
      productionTip: true,
      /**
       * Whether to enable devtools
       */
      devtools: true,
      /**
       * Whether to record perf
       */
      performance: false,
      /**
       * Error handler for watcher errors
       */
      errorHandler: null,
      /**
       * Warn handler for watcher warns
       */
      warnHandler: null,
      /**
       * Ignore certain custom elements
       */
      ignoredElements: [],
      /**
       * Custom user key aliases for v-on
       */
      // $flow-disable-line
      keyCodes: Object.create(null),
      /**
       * Check if a tag is reserved so that it cannot be registered as a
       * component. This is platform-dependent and may be overwritten.
       */
      isReservedTag: no,
      /**
       * Check if an attribute is reserved so that it cannot be used as a component
       * prop. This is platform-dependent and may be overwritten.
       */
      isReservedAttr: no,
      /**
       * Check if a tag is an unknown element.
       * Platform-dependent.
       */
      isUnknownElement: no,
      /**
       * Get the namespace of an element
       */
      getTagNamespace: noop,
      /**
       * Parse the real tag name for the specific platform.
       */
      parsePlatformTagName: identity,
      /**
       * Check if an attribute must be bound using property, e.g. value
       * Platform-dependent.
       */
      mustUseProp: no,
      /**
       * Perform updates asynchronously. Intended to be used by Vue Test Utils
       * This will significantly reduce performance if set to false.
       */
      async: true,
      /**
       * Exposed for legacy reasons
       */
      _lifecycleHooks: LIFECYCLE_HOOKS
  };

  /**
   * unicode letters used for parsing html tags, component names and property paths.
   * using https://www.w3.org/TR/html53/semantics-scripting.html#potentialcustomelementname
   * skipping \u10000-\uEFFFF due to it freezing up PhantomJS
   */
  var unicodeRegExp = /a-zA-Z\u00B7\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u037D\u037F-\u1FFF\u200C-\u200D\u203F-\u2040\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD/;
  /**
   * Check if a string starts with $ or _
   */
  function isReserved(str) {
      var c = (str + '').charCodeAt(0);
      return c === 0x24 || c === 0x5f;
  }
  /**
   * Define a property.
   */
  function def(obj, key, val, enumerable) {
      Object.defineProperty(obj, key, {
          value: val,
          enumerable: !!enumerable,
          writable: true,
          configurable: true
      });
  }
  /**
   * Parse simple path.
   */
  var bailRE = new RegExp("[^".concat(unicodeRegExp.source, ".$_\\d]"));
  function parsePath(path) {
      if (bailRE.test(path)) {
          return;
      }
      var segments = path.split('.');
      return function (obj) {
          for (var i = 0; i < segments.length; i++) {
              if (!obj)
                  return;
              obj = obj[segments[i]];
          }
          return obj;
      };
  }

  // can we use __proto__?
  var hasProto = '__proto__' in {};
  // Browser environment sniffing
  var inBrowser = typeof window !== 'undefined';
  var UA = inBrowser && window.navigator.userAgent.toLowerCase();
  var isIE = UA && /msie|trident/.test(UA);
  var isIE9 = UA && UA.indexOf('msie 9.0') > 0;
  var isEdge = UA && UA.indexOf('edge/') > 0;
  UA && UA.indexOf('android') > 0;
  var isIOS = UA && /iphone|ipad|ipod|ios/.test(UA);
  UA && /chrome\/\d+/.test(UA) && !isEdge;
  UA && /phantomjs/.test(UA);
  var isFF = UA && UA.match(/firefox\/(\d+)/);
  // Firefox has a "watch" function on Object.prototype...
  // @ts-expect-error firebox support
  var nativeWatch = {}.watch;
  var supportsPassive = false;
  if (inBrowser) {
      try {
          var opts = {};
          Object.defineProperty(opts, 'passive', {
              get: function () {
                  /* istanbul ignore next */
                  supportsPassive = true;
              }
          }); // https://github.com/facebook/flow/issues/285
          window.addEventListener('test-passive', null, opts);
      }
      catch (e) { }
  }
  // this needs to be lazy-evaled because vue may be required before
  // vue-server-renderer can set VUE_ENV
  var _isServer;
  var isServerRendering = function () {
      if (_isServer === undefined) {
          /* istanbul ignore if */
          if (!inBrowser && typeof global !== 'undefined') {
              // detect presence of vue-server-renderer and avoid
              // Webpack shimming the process
              _isServer =
                  global['process'] && global['process'].env.VUE_ENV === 'server';
          }
          else {
              _isServer = false;
          }
      }
      return _isServer;
  };
  // detect devtools
  var devtools = inBrowser && window.__VUE_DEVTOOLS_GLOBAL_HOOK__;
  /* istanbul ignore next */
  function isNative(Ctor) {
      return typeof Ctor === 'function' && /native code/.test(Ctor.toString());
  }
  var hasSymbol = typeof Symbol !== 'undefined' &&
      isNative(Symbol) &&
      typeof Reflect !== 'undefined' &&
      isNative(Reflect.ownKeys);
  var _Set; // $flow-disable-line
  /* istanbul ignore if */ if (typeof Set !== 'undefined' && isNative(Set)) {
      // use native Set when available.
      _Set = Set;
  }
  else {
      // a non-standard Set polyfill that only works with primitive keys.
      _Set = /** @class */ (function () {
          function Set() {
              this.set = Object.create(null);
          }
          Set.prototype.has = function (key) {
              return this.set[key] === true;
          };
          Set.prototype.add = function (key) {
              this.set[key] = true;
          };
          Set.prototype.clear = function () {
              this.set = Object.create(null);
          };
          return Set;
      }());
  }

  var currentInstance = null;
  /**
   * This is exposed for compatibility with v3 (e.g. some functions in VueUse
   * relies on it). Do not use this internally, just use `currentInstance`.
   *
   * @internal this function needs manual type declaration because it relies
   * on previously manually authored types from Vue 2
   */
  function getCurrentInstance() {
      return currentInstance && { proxy: currentInstance };
  }
  /**
   * @internal
   */
  function setCurrentInstance(vm) {
      if (vm === void 0) { vm = null; }
      if (!vm)
          currentInstance && currentInstance._scope.off();
      currentInstance = vm;
      vm && vm._scope.on();
  }

  /**
   * @internal
   */
  var VNode = /** @class */ (function () {
      function VNode(tag, data, children, text, elm, context, componentOptions, asyncFactory) {
          this.tag = tag;
          this.data = data;
          this.children = children;
          this.text = text;
          this.elm = elm;
          this.ns = undefined;
          this.context = context;
          this.fnContext = undefined;
          this.fnOptions = undefined;
          this.fnScopeId = undefined;
          this.key = data && data.key;
          this.componentOptions = componentOptions;
          this.componentInstance = undefined;
          this.parent = undefined;
          this.raw = false;
          this.isStatic = false;
          this.isRootInsert = true;
          this.isComment = false;
          this.isCloned = false;
          this.isOnce = false;
          this.asyncFactory = asyncFactory;
          this.asyncMeta = undefined;
          this.isAsyncPlaceholder = false;
      }
      Object.defineProperty(VNode.prototype, "child", {
          // DEPRECATED: alias for componentInstance for backwards compat.
          /* istanbul ignore next */
          get: function () {
              return this.componentInstance;
          },
          enumerable: false,
          configurable: true
      });
      return VNode;
  }());
  var createEmptyVNode = function (text) {
      if (text === void 0) { text = ''; }
      var node = new VNode();
      node.text = text;
      node.isComment = true;
      return node;
  };
  function createTextVNode(val) {
      return new VNode(undefined, undefined, undefined, String(val));
  }
  // optimized shallow clone
  // used for static nodes and slot nodes because they may be reused across
  // multiple renders, cloning them avoids errors when DOM manipulations rely
  // on their elm reference.
  function cloneVNode(vnode) {
      var cloned = new VNode(vnode.tag, vnode.data, 
      // #7975
      // clone children array to avoid mutating original in case of cloning
      // a child.
      vnode.children && vnode.children.slice(), vnode.text, vnode.elm, vnode.context, vnode.componentOptions, vnode.asyncFactory);
      cloned.ns = vnode.ns;
      cloned.isStatic = vnode.isStatic;
      cloned.key = vnode.key;
      cloned.isComment = vnode.isComment;
      cloned.fnContext = vnode.fnContext;
      cloned.fnOptions = vnode.fnOptions;
      cloned.fnScopeId = vnode.fnScopeId;
      cloned.asyncMeta = vnode.asyncMeta;
      cloned.isCloned = true;
      return cloned;
  }

  /* not type checking this file because flow doesn't play well with Proxy */
  var initProxy;
  {
      var allowedGlobals_1 = makeMap('Infinity,undefined,NaN,isFinite,isNaN,' +
          'parseFloat,parseInt,decodeURI,decodeURIComponent,encodeURI,encodeURIComponent,' +
          'Math,Number,Date,Array,Object,Boolean,String,RegExp,Map,Set,JSON,Intl,BigInt,' +
          'require' // for Webpack/Browserify
      );
      var warnNonPresent_1 = function (target, key) {
          warn$2("Property or method \"".concat(key, "\" is not defined on the instance but ") +
              'referenced during render. Make sure that this property is reactive, ' +
              'either in the data option, or for class-based components, by ' +
              'initializing the property. ' +
              'See: https://v2.vuejs.org/v2/guide/reactivity.html#Declaring-Reactive-Properties.', target);
      };
      var warnReservedPrefix_1 = function (target, key) {
          warn$2("Property \"".concat(key, "\" must be accessed with \"$data.").concat(key, "\" because ") +
              'properties starting with "$" or "_" are not proxied in the Vue instance to ' +
              'prevent conflicts with Vue internals. ' +
              'See: https://v2.vuejs.org/v2/api/#data', target);
      };
      var hasProxy_1 = typeof Proxy !== 'undefined' && isNative(Proxy);
      if (hasProxy_1) {
          var isBuiltInModifier_1 = makeMap('stop,prevent,self,ctrl,shift,alt,meta,exact');
          config.keyCodes = new Proxy(config.keyCodes, {
              set: function (target, key, value) {
                  if (isBuiltInModifier_1(key)) {
                      warn$2("Avoid overwriting built-in modifier in config.keyCodes: .".concat(key));
                      return false;
                  }
                  else {
                      target[key] = value;
                      return true;
                  }
              }
          });
      }
      var hasHandler_1 = {
          has: function (target, key) {
              var has = key in target;
              var isAllowed = allowedGlobals_1(key) ||
                  (typeof key === 'string' &&
                      key.charAt(0) === '_' &&
                      !(key in target.$data));
              if (!has && !isAllowed) {
                  if (key in target.$data)
                      warnReservedPrefix_1(target, key);
                  else
                      warnNonPresent_1(target, key);
              }
              return has || !isAllowed;
          }
      };
      var getHandler_1 = {
          get: function (target, key) {
              if (typeof key === 'string' && !(key in target)) {
                  if (key in target.$data)
                      warnReservedPrefix_1(target, key);
                  else
                      warnNonPresent_1(target, key);
              }
              return target[key];
          }
      };
      initProxy = function initProxy(vm) {
          if (hasProxy_1) {
              // determine which proxy handler to use
              var options = vm.$options;
              var handlers = options.render && options.render._withStripped ? getHandler_1 : hasHandler_1;
              vm._renderProxy = new Proxy(vm, handlers);
          }
          else {
              vm._renderProxy = vm;
          }
      };
  }

  /******************************************************************************
  Copyright (c) Microsoft Corporation.

  Permission to use, copy, modify, and/or distribute this software for any
  purpose with or without fee is hereby granted.

  THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
  REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
  AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
  INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
  LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
  OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OF
  PERFORMANCE OF THIS SOFTWARE.
  ***************************************************************************** */

  var __assign = function() {
      __assign = Object.assign || function __assign(t) {
          for (var s, i = 1, n = arguments.length; i < n; i++) {
              s = arguments[i];
              for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p)) t[p] = s[p];
          }
          return t;
      };
      return __assign.apply(this, arguments);
  };

  typeof SuppressedError === "function" ? SuppressedError : function (error, suppressed, message) {
      var e = new Error(message);
      return e.name = "SuppressedError", e.error = error, e.suppressed = suppressed, e;
  };

  var uid$2 = 0;
  var pendingCleanupDeps = [];
  var cleanupDeps = function () {
      for (var i = 0; i < pendingCleanupDeps.length; i++) {
          var dep = pendingCleanupDeps[i];
          dep.subs = dep.subs.filter(function (s) { return s; });
          dep._pending = false;
      }
      pendingCleanupDeps.length = 0;
  };
  /**
   * A dep is an observable that can have multiple
   * directives subscribing to it.
   * @internal
   */
  var Dep = /** @class */ (function () {
      function Dep() {
          // pending subs cleanup
          this._pending = false;
          this.id = uid$2++;
          this.subs = [];
      }
      Dep.prototype.addSub = function (sub) {
          this.subs.push(sub);
      };
      Dep.prototype.removeSub = function (sub) {
          // #12696 deps with massive amount of subscribers are extremely slow to
          // clean up in Chromium
          // to workaround this, we unset the sub for now, and clear them on
          // next scheduler flush.
          this.subs[this.subs.indexOf(sub)] = null;
          if (!this._pending) {
              this._pending = true;
              pendingCleanupDeps.push(this);
          }
      };
      Dep.prototype.depend = function (info) {
          if (Dep.target) {
              Dep.target.addDep(this);
              if (info && Dep.target.onTrack) {
                  Dep.target.onTrack(__assign({ effect: Dep.target }, info));
              }
          }
      };
      Dep.prototype.notify = function (info) {
          // stabilize the subscriber list first
          var subs = this.subs.filter(function (s) { return s; });
          if (!config.async) {
              // subs aren't sorted in scheduler if not running async
              // we need to sort them now to make sure they fire in correct
              // order
              subs.sort(function (a, b) { return a.id - b.id; });
          }
          for (var i = 0, l = subs.length; i < l; i++) {
              var sub = subs[i];
              if (info) {
                  sub.onTrigger &&
                      sub.onTrigger(__assign({ effect: subs[i] }, info));
              }
              sub.update();
          }
      };
      return Dep;
  }());
  // The current target watcher being evaluated.
  // This is globally unique because only one watcher
  // can be evaluated at a time.
  Dep.target = null;
  var targetStack = [];
  function pushTarget(target) {
      targetStack.push(target);
      Dep.target = target;
  }
  function popTarget() {
      targetStack.pop();
      Dep.target = targetStack[targetStack.length - 1];
  }

  /*
   * not type checking this file because flow doesn't play well with
   * dynamically accessing methods on Array prototype
   */
  var arrayProto = Array.prototype;
  var arrayMethods = Object.create(arrayProto);
  var methodsToPatch = [
      'push',
      'pop',
      'shift',
      'unshift',
      'splice',
      'sort',
      'reverse'
  ];
  /**
   * Intercept mutating methods and emit events
   */
  methodsToPatch.forEach(function (method) {
      // cache original method
      var original = arrayProto[method];
      def(arrayMethods, method, function mutator() {
          var args = [];
          for (var _i = 0; _i < arguments.length; _i++) {
              args[_i] = arguments[_i];
          }
          var result = original.apply(this, args);
          var ob = this.__ob__;
          var inserted;
          switch (method) {
              case 'push':
              case 'unshift':
                  inserted = args;
                  break;
              case 'splice':
                  inserted = args.slice(2);
                  break;
          }
          if (inserted)
              ob.observeArray(inserted);
          // notify change
          {
              ob.dep.notify({
                  type: "array mutation" /* TriggerOpTypes.ARRAY_MUTATION */,
                  target: this,
                  key: method
              });
          }
          return result;
      });
  });

  var arrayKeys = Object.getOwnPropertyNames(arrayMethods);
  var NO_INITIAL_VALUE = {};
  /**
   * In some cases we may want to disable observation inside a component's
   * update computation.
   */
  var shouldObserve = true;
  function toggleObserving(value) {
      shouldObserve = value;
  }
  // ssr mock dep
  var mockDep = {
      notify: noop,
      depend: noop,
      addSub: noop,
      removeSub: noop
  };
  /**
   * Observer class that is attached to each observed
   * object. Once attached, the observer converts the target
   * object's property keys into getter/setters that
   * collect dependencies and dispatch updates.
