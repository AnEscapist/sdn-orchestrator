# vue-transform
Vue json based form, modal with bootstrap3  
[Live Demo](http://marcodpt.github.io/vue-transform)
 - display an object in a reasonable way
 - very quick form build
 - modal using root scope
 - very nice form automatic builded with props of your component (good for tests and create live demo)

## Install
```
npm install --save vue-transform
```

## Usage

```javascript
  import Vue from 'vue'
  import {transform, modal} from 'vue-transform'

  new Vue({
    components: {
      transform: transform,
      modal: modal
    },
    data: {
      "form": {
        "value": 5,
        "info": "Test",
        "date": "2018-04-01"
      },
      "modal": {
        "text": "Some message for user"
      },
      "test": {}
    },
    methods: {
      showModal: function () {
        this.$root.$data.modal = this.$data.modal
      }
    }
  }).$mount('#app')
```

You must use with **bootstrap3** css, or send a pull request with other frameworks :)

Form usage
```html
  <transform :model="form" />
```

Modal usage
```html
  <button @click="showModal">Show Modal</button>
  <modal />
```

Test your component usage
```html
  <transform :model="test" :fields="$options.components['myComponent'].props" />
```

### Props
 - model 
   - type: Object
   - default: {}
   - description: form model
 - fields
   - type: Array, Object
   - default: none
   - description: if you pass nothing it will create an array based on your model, if you pass an object it will think that is the props of some component you want to test, finally if you pass an array it will act strictly the way you want, see **item** below for description of array objects
 - submit
   - type: Function
   - default: none
   - description: function that will be called when submitted, it pass as a parameter the current model
 - onChange 
   - type: Function
   - default: none
   - description: just like submit but it act on every model change
 - onClose
   - type: Function
   - default: none
   - description: it is useful with modal or if you want a close button on your form
 - size
   - type: String
   - default: md
   - description: quick adjustment of form size
 - icon
   - type: String
   - default: ''
   - description: One of **vue-awesome** icons to be placed near form title
 - label
   - type: String
   - default: ''
   - description: Form title
 - alert
   - type: String
   - default: danger
   - description: **bootstrap3** alert type
 - text
   - type: String
   - default: ''
   - description: Alert text, alerts are specially useful with **modal**
 - buttons
   - type: Array
   - default: []
   - description: Array of buttons, see **button**  below

#### Item
 - Array of fields item (Object), props:
   - id
     - type: String
     - default: ''
     - description: **model** key of field
   - label
     - type: String
     - default: if nothing is passed same string as **id**
     - description: label for the field
   - static
     - type: Boolean
     - default: false
     - description: field is input or just static field, observe that even static = false must pass a **submit** function for field not be static
   - col 
     - type: Number
     - default: 1
     - description: from 0 to 4, 0 means without label full width, 1 is 100%, 2 is 50%, 3 is 33% and 4 is 25% 
   - format
     - type: String
     - default: string
     - description: boolean, integer, number, date, string
   - size
     - type: String
     - default: md
     - description: field only adjustment of size
   - Validate
     - type: Array
     - default: []
     - description: submit function will only be called if all validation of all fields pass
     - items (Object): 
       - assert
         - type: String
         - description: condition to be evaluated, use **$** to refer to form model 
       - error
         - type: String
         - description: error message in case of validation fail

#### Button
 - Array of buttons item (Object), props:
   - type 
     - type: String
     - default: ''
     - description: One of **bootstrap3** buttons types, like danger, success, warning...
   - size
     - type: String,
     - default: md
     - description: One of **bootstrap3** buttons sizes, like md, lg, sm, xs
   - block: 
     - type: Boolean
     - default: false
     - description: Full width button?
   - icon
     - type: String
     - default: ''
     - description: One of **vue-awesome** icons to be placed before button label
   - label
     - type: String
     - default: ''
     - description: Button label
   - click
     - type: Function
     - default: none
     - description: If none is passed it will use transform **submit** otherwise click function

## Contribute
We need help! Our goals are:
 - Separate classes and styles in order to add more css frameworks
 - Change props api in order to correctly support other css frameworks
 - Add more css frameworks like bootstrap4, bulma and foundation
 - Implement in the correct way modal (maybe as a plugin) without root scope
 - Implement in the correct way the test usage
 - Add tests
 - More usage examples and better home page
 - Add support to most browsers
