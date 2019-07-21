# vue-inputag
All html inputs in a single vue component
[Live Demo](http://marcodpt.github.io/vue-inputag)

## Install
```
npm install --save vue-inputag
```

## Usage
```javascript
  import Vue from '../node_modules/vue/dist/vue.js'
  import inputag from './index.vue'

  new Vue({
    components: {
      'vue-inputag': inputag
    },
    data: {
      model: {
        number: 3.14,
        integer: 25,
        date: '2018-01-01',
        string: 'Fork me on github',
        text: 'This is a sample text\nEdit as many times as you want',
        scientist: 'Gauss',
        country: 2,
        file: null,
        msg: 'hello world!',
        button: 'alert!'
      },
      click: (data) => {window.alert(data.msg)},
      github: 'https://github.com/marcodpt/vue-inputag',
      options: [
        "Eistein",
        "Newton",
        "Gauss",
        "Euler",
        "Riemann"
      ],
      options2: [
        {
          id: 1,
          label: 'Italy'
        }, {
          id: 2,
          label: 'France'
        }, {
          id: 3,
          label: 'Germany'
        }, {
          id: 4,
          label: 'England'
        }
      ]
    }
  }).$mount('#app')
```

```html
  <div style="margin:20px">
    <label>String: <vue-inputag :href="github" :model="model" id="string" type=""/></label> 
    <div>
      <vue-inputag :model="model" id="string"/>
    </div>
  </div>
  <div style="margin:20px">
    <label>Button: <vue-inputag :click="click" :model="model" id="button" type=""/></label> 
    <div>
      <vue-inputag :model="model" id="msg"/>
    </div>
  </div>
  <div style="margin:20px">
    <label>Text: <vue-inputag :model="model" id="text" type=""/></label> 
    <div>
      <vue-inputag :model="model" id="text" type="textarea"/>
    </div>
  </div>
  <div style="margin:20px">
    <label>Number: <vue-inputag :model="model" id="number" type=""/></label> 
    <div>
      <vue-inputag :model="model" id="number" type="number"/>
    </div>
  </div>
  <div style="margin:20px">
    <label>Date: <vue-inputag :model="model" id="date" type=""/></label> 
    <div>
      <vue-inputag :model="model" id="date" type="date"/>
    </div>
  </div>
  <div style="margin:20px">
    <label>File: <vue-inputag :model="model" id="file" type=""/></label> 
    <div>
      <vue-inputag :model="model" id="file" type="file"/>
    </div>
  </div>
  <div style="margin:20px">
    <label>Progress: <vue-inputag :model="model" id="integer" type="progressbar" style="width:250px"/></label> 
    <div>
      <vue-inputag :model="model" id="integer" type="range"/>
    </div>
  </div>
  <div style="margin:20px">
    <label>Simple Select: <vue-inputag :model="model" id="scientist" type=""/></label> 
    <div>
      <vue-inputag :model="model" id="scientist" type="select" :options="options"/>
    </div>
  </div>
  <div style="margin:20px">
    <label>(id/label) Select: <vue-inputag :model="model" id="country" type=""/></label> 
    <div>
      <vue-inputag :model="model" id="country" type="select" :options="options2"/>
    </div>
  </div>
```

### Props
 - model 
   - type: Object
   - required: true
   - description: Object model
 - id
   - type: String
   - required: true
   - description: variable id inside object
 - type
   - type: String
   - default: "text"
   - description: Any input type from html5 + select + textarea + progressbar + pass blank type to static string or with an href become a link or with click become a button
 - formatter
   - type: Function
   - default: x => x
   - description: Function to format model[id] in case of type of input is blank
 - click
   - type: Function
   - default: undefined
   - description: in case of type is blank string and function passed it will render button
 - href
   - type: String
   - default: ""
   - description: in case of type is blank string and href passed it will render link, you can use :variable and it will render correct based on model
 - dependencies
   - type: Array
   - default: []
   - description: (select only) what model fields should not be null before trigger source
 - options
   - type: Array
   - default: []
   - description: (select only) array of options, you can use {id, label} object if needed
 - source
   - type: Function
   - default: function (model, callback) {  
      callback(this.options)  
    }  
   - description: (select only) function that calls options
 - required
   - type: Boolean
   - default: false
   - description: (select only) is required to fill with one of the options?

  All other props are bypassed to html element, even styles and classes  
  You should obseve that we use vue-select in case of select and only in this case  
  it is better not pass any style or class 

### Slot
  When type is a blank string it will render: 
   - a button if has a click function 
   - a link if has a href
   - span otherwise
   - all 3 cases admit slot, all other cases not

## Contribute
We need help! Our goals are:
 - Support an easy and quick api interface for input and output any kind of data
 - Add tests
 - More usage examples and better home page
 - Add support to most browsers

What is outside of the scope of this project:
 - Use any kind of css framework or any layout decision
