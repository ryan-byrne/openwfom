(this.webpackJsonpclient=this.webpackJsonpclient||[]).push([[0],{62:function(e,t,n){"use strict";n.r(t);var c=n(0),a=n(24),r=n.n(a),i=(n(56),n(48)),s=n(27),j=n(7),o=n(30),l=n(25),d=n(39),b=n(9),O=n(1);function h(){return Object(O.jsxs)(l.a,{children:[Object(O.jsxs)(o.a,{className:"m-3",children:[Object(O.jsx)(j.a.Control,{type:"text",placeholder:"Enter UNI"}),Object(O.jsx)(j.a.Control,{className:"ml-3",type:"text",placeholder:"Mouse ID"})]}),Object(O.jsxs)(o.a,{className:"m-3",children:[Object(O.jsx)(j.a.Control,{type:"number",placeholder:"Run Length",min:"0",step:"0.01"}),Object(O.jsxs)(j.a.Control,{className:"mr-5",as:"select",children:[Object(O.jsx)("option",{children:"Sec"}),Object(O.jsx)("option",{children:"Min"}),Object(O.jsx)("option",{children:"Hr"})]}),Object(O.jsx)(j.a.Control,{className:"ml-3",type:"number",placeholder:"Number of Runs",min:"0",step:"1"})]}),Object(O.jsx)(o.a,{className:"m-3",children:Object(O.jsx)(j.a.File,{})}),Object(O.jsxs)(d.a,{className:"float-right",children:[Object(O.jsx)(b.a,{variant:"secondary",children:"Close"}),Object(O.jsx)(b.a,{variant:"secondary",className:"ml-1 mr-1",children:"Set Default"}),Object(O.jsx)(b.a,{children:"Start Acquisition"})]})]})}var u=n(17),x=n(14),f=n(16),m=n(35),p=n(32),g=n(36),C=n(51),v=n(8),y=function(e){var t=Object(c.useState)([]),n=Object(x.a)(t,2),a=n[0],r=n[1];return Object(c.useEffect)((function(){fetch("/find/cameras").then((function(e){return e.json().then((function(e){return r(e)}))}))}),[]),Object(O.jsxs)(f.a,{show:e.show,onHide:e.handleAdd,children:[Object(O.jsx)(f.a.Header,{closeButton:!0}),Object(O.jsxs)(f.a.Body,{children:[Object(O.jsx)(f.a.Title,{children:"Available Cameras"}),0===a.length?Object(O.jsxs)(p.a,{variant:"info",children:[Object(O.jsx)(m.a,{animation:"border",size:"sm",className:"mr-3"}),"Searching for Cameras"]}):Object(O.jsx)(g.a,{children:Object(O.jsxs)("tbody",{children:[Object(O.jsxs)("tr",{children:[Object(O.jsx)("th",{}),Object(O.jsx)("th",{children:"Device"}),Object(O.jsx)("th",{children:"Index"})]}),a.map((function(t,n){return Object(O.jsxs)("tr",{children:[Object(O.jsx)("td",{children:Object(O.jsx)(b.a,{onClick:function(t){return function(t,n){t.target.textContent="Adding...";var c=Object(u.a)(a),i=c.pop(n);fetch("/connect/camera/",{method:"POST",headers:{Accept:"application/json","Content-Type":"application/json"},body:JSON.stringify(i)}).then((function(t){return t.json().then((function(t){e.setCurrentCameras([].concat(Object(u.a)(e.currentCameras),[i])),r(c)}))}))}(t,n)},children:"Add"})}),Object(O.jsx)("td",{children:t.device}),Object(O.jsx)("td",{children:t.index})]},n)}))]})}),Object(O.jsx)(f.a.Title,{children:"Current Cameras"}),0===e.currentCameras.length?Object(O.jsx)(p.a,{variant:"warning",children:"No Cameras Added"}):Object(O.jsx)(g.a,{children:Object(O.jsxs)("tbody",{className:"text-center",children:[Object(O.jsxs)("tr",{children:[Object(O.jsx)("th",{}),Object(O.jsx)("th",{children:"Master"}),Object(O.jsx)("th",{children:"Name"}),Object(O.jsx)("th",{children:"Type"}),Object(O.jsx)("th",{children:"Index"})]}),e.currentCameras.map((function(t,n){return Object(O.jsxs)("tr",{children:[Object(O.jsx)("td",{children:Object(O.jsx)(b.a,{onClick:function(){return function(t){fetch("/close/camera/"+t.toString(),{method:"POST"}).then((function(n){return n.json().then((function(n){var c=Object(u.a)(e.currentCameras);r([].concat(Object(u.a)(a),[c.pop(t)])),e.setCurrentCameras(c)}))}))}(n)},children:"Remove"})}),Object(O.jsx)("td",{children:Object(O.jsx)(j.a.Check,{})}),Object(O.jsx)("td",{children:Object(O.jsx)(j.a.Control,{type:"text"})}),Object(O.jsx)("td",{children:t.device}),Object(O.jsx)("td",{children:t.index})]},n)}))]})})]}),Object(O.jsxs)(f.a.Footer,{children:[Object(O.jsx)(b.a,{onClick:e.handleAdd,variant:"secondary",children:"Close"}),Object(O.jsx)(b.a,{variant:"primary",children:"Save changes"})]})]})};function S(){var e=Object(c.useState)(!1),t=Object(x.a)(e,2),n=t[0],a=t[1],r=Object(c.useState)([]),i=Object(x.a)(r,2),s=i[0],j=i[1],o=Object(c.useState)(0),d=Object(x.a)(o,2);d[0],d[1];return Object(O.jsxs)(l.a,{className:"text-center mt-3",children:[0===s.length?null:s.map((function(e,t){return Object(O.jsx)(v.a,{children:Object(O.jsx)(C.a,{fluid:!0,src:"/feed/"+t.toString()})})})),Object(O.jsx)(b.a,{className:"m-3",onClick:function(){return a(!0)},children:"Edit Camera(s)"}),Object(O.jsx)(y,{show:n,handleAdd:function(e){return a(!n)},currentCameras:s,setCurrentCameras:j})]})}var N=n(10),A=n(13),T=function(e){var t=function(t,n,c){var a=Object(u.a)(e.leds);a[t][c]=n,e.setConfig(Object(N.a)(Object(N.a)({},e.config),{},{leds:a}))};return Object(O.jsx)(j.a,{children:Object(O.jsxs)(l.a,{children:[Object(O.jsx)(A.a,{}),Object(O.jsxs)(A.a,{children:[Object(O.jsx)(v.a,{}),Object(O.jsxs)(v.a,{children:[Object(O.jsx)(j.a.Control,{type:"number",min:"0",step:"1",placeholder:"Trigger Pin",onChange:function(t){return n=t.target.value,e.setConfig(Object(N.a)(Object(N.a)({},e.config),{},{trig:n}));var n}}),Object(O.jsx)(j.a.Text,{className:"text-muted",children:"Set the Trigger Pin"})]}),Object(O.jsx)(v.a,{})]}),e.config.leds.map((function(e,n){return Object(O.jsxs)(A.a,{children:[Object(O.jsx)(v.a,{children:Object(O.jsx)(j.a.Control,{type:"text",placeholder:"LED Name",onChange:function(e){return t(n,e.target.value,"name")}})}),Object(O.jsx)(v.a,{children:Object(O.jsx)(j.a.Control,{type:"number",min:"0",step:"1",placeholder:"LED Pin",onChange:function(e){return t(n,e.target.value,"pin")}})}),Object(O.jsx)(v.a,{children:Object(O.jsx)(b.a,{variant:"secondary",children:"Remove"})}),Object(O.jsx)(v.a,{children:Object(O.jsx)(b.a,{variant:"primary",children:"Test"})})]},n)})),Object(O.jsxs)(A.a,{children:[Object(O.jsx)(v.a,{}),Object(O.jsx)(v.a,{children:Object(O.jsx)(b.a,{onClick:function(t){e.setConfig(Object(N.a)(Object(N.a)({},e.config),{},{leds:[].concat(Object(u.a)(e.config.leds),[{name:"New Lew",pin:0}])}))},children:"Add LED"})}),Object(O.jsx)(v.a,{})]}),Object(O.jsx)(j.a.Text,{className:"text-muted",children:"Configure LEDs"})]})})},k=function(e){var t=function(t,n,c){var a=Object(u.a)(e.config.stim);"type"===c&&n.target.value!==e.stim[t].type&&("4PinStepper"===n.target.value?a[t].pins.push("0","1"):a[t].pins.splice(-2,2)),a[t][c]=n.target.value,e.setConfig(Object(N.a)(Object(N.a)({},e.config),{},{stim:a}))};return Object(O.jsxs)(j.a,{children:[Object(O.jsx)(j.a.Group,{as:A.a}),Object(O.jsx)(j.a.Group,{controlId:"stims",children:e.config.stim.map((function(n,c){return Object(O.jsxs)(l.a,{children:[Object(O.jsxs)(A.a,{children:[Object(O.jsx)(v.a,{children:Object(O.jsx)(j.a.Control,{type:"text",placeholder:"Stim Name",onChange:function(e){return t(c,e,"name")}})}),Object(O.jsx)(v.a,{children:Object(O.jsxs)(j.a.Control,{onChange:function(e){return t(c,e,"type")},as:"select",children:[Object(O.jsx)("option",{children:"2PinStepper"}),Object(O.jsx)("option",{children:"4PinStepper"})]})}),Object(O.jsx)(v.a,{children:Object(O.jsx)(b.a,{variant:"secondary",onClick:function(){return function(t){var n=Object(u.a)(e.config.stim);n.splice(t,1),e.setConfig(Object(N.a)(Object(N.a)({},e.config),{},{stim:n}))}(c)},children:"Remove"})}),Object(O.jsx)(v.a,{children:Object(O.jsx)(b.a,{variant:"primary",children:"Test"})})]},c),n.pins.map((function(t,n){return Object(O.jsx)(A.a,{children:Object(O.jsx)(j.a.Control,{type:"number",min:"0",step:"1",placeholder:"Pin",onChange:function(t){return function(t,n,c){var a=Object(u.a)(e.config.stim);a[n].pins[c]=t.target.value,e.setConfig(Object(N.a)(Object(N.a)({},e.config),{},{stim:a}))}(t,c,n)}})})}))]})}))}),Object(O.jsxs)(j.a.Group,{children:[Object(O.jsxs)(A.a,{children:[Object(O.jsx)(v.a,{}),Object(O.jsx)(v.a,{children:Object(O.jsx)(b.a,{onClick:function(t){e.setConfig(Object(N.a)(Object(N.a)({},e.config),{},{stim:[].concat(Object(u.a)(e.config.stim),[{name:"",type:"2PinStepper",pins:["0","1"]}])}))},children:"Add Stim"})}),Object(O.jsx)(v.a,{})]}),Object(O.jsx)(A.a,{children:Object(O.jsx)(v.a,{children:Object(O.jsx)(j.a.Text,{className:"text-muted",children:"Configure Stim"})})})]})]})},w=function(e){return Object(O.jsxs)(j.a,{children:[Object(O.jsx)(j.a.Group,{as:A.a}),Object(O.jsx)(j.a.Group,{controlId:"stims",children:e.config.daq.map((function(t,n){return Object(O.jsxs)(A.a,{children:[Object(O.jsx)(v.a,{children:Object(O.jsx)(j.a.Control,{type:"text",placeholder:"DAQ Name"})}),Object(O.jsx)(v.a,{children:Object(O.jsx)(j.a.Control,{type:"number",min:"0",step:"1",placeholder:"DAQ Pin"})}),Object(O.jsx)(v.a,{children:Object(O.jsx)(b.a,{onClick:function(t){return function(t){var n=e.config.daq;n.splice(t,1),e.setConfig(Object(N.a)(Object(N.a)({},e.config),{},{daq:n}))}(n)},variant:"secondary",children:"Remove"})}),Object(O.jsx)(v.a,{children:Object(O.jsx)(b.a,{variant:"primary",children:"Test"})})]},n)}))}),Object(O.jsxs)(j.a.Group,{children:[Object(O.jsx)(A.a,{children:Object(O.jsx)(v.a,{children:Object(O.jsx)(b.a,{onClick:function(t){return e.setConfig(Object(N.a)(Object(N.a)({},e.config),{},{daq:[{name:"New DAQ",pin:0}]}))},children:"Add DAQ"})})}),Object(O.jsx)(A.a,{children:Object(O.jsx)(v.a,{children:Object(O.jsx)(j.a.Text,{className:"text-muted",children:"Configure Data Acquisition"})})})]})]})},D=function(e){var t=Object(c.useState)(!1),n=Object(x.a)(t,2),a=n[0],r=(n[1],Object(c.useState)({device:"arduino",leds:[],daq:[],port:null,trig:null,stim:[]})),j=Object(x.a)(r,2),o=j[0],l=j[1];return Object(c.useEffect)((function(){fetch("/settings/arduino/get").then((function(e){return e.json().then((function(e){return console.log(e)}))}))}),[]),Object(O.jsxs)(f.a,{show:e.show,onHide:e.handleConfig,children:[Object(O.jsx)(f.a.Header,{closeButton:!0,children:Object(O.jsx)(f.a.Title,{children:"Arduino Configuration"})}),Object(O.jsx)(f.a.Body,{children:Object(O.jsxs)(i.a,{children:[Object(O.jsx)(s.a,{eventKey:"strobingTab",title:"Strobing",children:Object(O.jsx)(T,{config:o,setConfig:l})}),Object(O.jsx)(s.a,{eventKey:"stimTab",title:"Stim",children:Object(O.jsx)(k,{config:o,setConfig:l})}),Object(O.jsx)(s.a,{eventKey:"daqTab",title:"Data Acquisition",children:Object(O.jsx)(w,{config:o,setConfig:l})})]})}),Object(O.jsxs)(f.a.Footer,{children:[Object(O.jsx)(b.a,{variant:"secondary",onClick:e.handleConfig,children:"Close"}),a?Object(O.jsxs)(b.a,{variant:"primary",disabled:!0,children:[Object(O.jsx)(m.a,{as:"span",size:"sm",animation:"border",role:"status"}),"Sending to Arduino"]}):Object(O.jsx)(b.a,{variant:"primary",onClick:function(){fetch("/api/connection/",{method:"POST",headers:{Accept:"application/json","Content-Type":"application/json"},body:JSON.stringify(o)}).then((function(e){return e.json().then((function(e){return console.log(e)})).catch((function(e){return console.log(e)}))})),e.handleConfig()},children:"Save Changes"})]})]})};function P(){var e=Object(c.useState)(!1),t=Object(x.a)(e,2),n=t[0],a=t[1],r=Object(c.useState)(!1),i=Object(x.a)(r,2),s=i[0],h=i[1],u=Object(c.useState)(null),f=Object(x.a)(u,2),C=f[0],v=f[1],y=Object(c.useState)(!0),S=Object(x.a)(y,2),N=S[0],A=S[1],T=Object(c.useState)([]),k=Object(x.a)(T,2),w=k[0],P=k[1],E=Object(c.useState)(0),R=Object(x.a)(E,2),q=R[0],I=R[1],K=function(){return a(!n)},F=function(){fetch("/find/arduinos").then((function(e){return e.json().then((function(e){return P(e)}))}))};return Object(c.useEffect)((function(){F()}),[]),Object(c.useEffect)((function(){0===w.length||(v(Object(O.jsxs)(p.a,{variant:"warning",children:[Object(O.jsx)(m.a,{animation:"border",className:"mr-3",size:"sm"}),"Connecting to ",Object(O.jsx)("b",{children:w[q].device}),"..."]})),fetch("/connect/arduino",{method:"POST",headers:{Accept:"application/json","Content-Type":"application/json"},body:JSON.stringify(w[q])}).then((function(e){return e.json().then((function(e){"error"===e.status&&(v(Object(O.jsx)(p.a,{variant:"danger",children:Object(O.jsxs)("p",{children:[Object(O.jsx)("b",{children:"ERROR:"})," Arduino at ",Object(O.jsx)("b",{children:w[q].device})," does not have compatible firmware.",Object(O.jsx)(b.a,{className:"ml-3",children:"Upload Firmware..."})]})})),A(!0))}))})))}),[w,q]),Object(O.jsxs)(l.a,{children:[Object(O.jsx)(j.a.Text,{className:"text-muted",children:"Select an Arduino"}),Object(O.jsxs)(o.a,{className:"text-center mb-3",children:[Object(O.jsx)(j.a.Control,{as:"select",custom:!0,children:0===w.length?Object(O.jsx)("option",{disabled:!0,defaultValue:!0,children:"No Arduinos Found."}):w.map((function(e,t){return Object(O.jsxs)("option",{onClick:function(){return I(t)},children:[e.product," - ",e.device]},t)}))}),Object(O.jsxs)(d.a,{children:[Object(O.jsx)(b.a,{variant:"secondary",onClick:function(){return F()},children:"Refresh"}),Object(O.jsx)(b.a,{variant:"secondary",onClick:function(){return h(!s)},disabled:0===w.length,children:s?"Hide Info":"Show Info"}),Object(O.jsx)(b.a,{variant:"primary",disabled:N,onClick:K,children:"Configure"})]})]}),Object(O.jsx)(D,{port:q,show:n,handleConfig:K}),C,s?Object(O.jsx)(g.a,{children:Object(O.jsx)("tbody",{children:Object.keys(w[q]).map((function(e,t){return Object(O.jsxs)("tr",{children:[Object(O.jsx)("th",{children:e.charAt(0).toUpperCase()+e.slice(1)}),Object(O.jsx)("td",{children:w[q][e]})]},t)}))})}):null]})}function E(){return Object(O.jsxs)(i.a,{defaultActiveKey:"profile",id:"uncontrolled-tab-example",children:[Object(O.jsx)(s.a,{eventKey:"runTab",title:"File",children:Object(O.jsx)(h,{})}),Object(O.jsx)(s.a,{eventKey:"camerasTab",title:"Cameras",children:Object(O.jsx)(S,{})}),Object(O.jsx)(s.a,{eventKey:"arduinoTab",title:"Arduino",children:Object(O.jsx)(P,{})})]})}r.a.render(Object(O.jsx)(E,{}),document.getElementById("root"))}},[[62,1,2]]]);
//# sourceMappingURL=main.db25d433.chunk.js.map