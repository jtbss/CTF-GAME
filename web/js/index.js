const app = Vue.createApp({
  data() {
    return {
      title: 'SSL simulator',
      show: false,
      cipher1: '',
      cipher2: '',
      form1: {},
      form2: {},
      rules: {
        key: [{ required: true, message: 'Please input key' }],
        message: [{ required: true, message: 'Please input message' }]
      },
      error: null,
      feedback: null
    }
  },
  methods: {
    toggleShow() {
      this.collapsed = !this.collapsed
    },
    onSendKey() {
      this.$refs.form1.validate(valid => {
        if (valid) {
          axios.post('/send_key', {
            key: this.form1.key
          })
            .then(response => {
              c1 = response.data.data1
              c2 = response.data.data2
              console.log(response)

              this.cipher1 = c1
              this.cipher2 = c2
            })
            .catch(error => {
              console.error(error)
            })
        }
      })
    },
    onSubmit() {
      this.$refs.form2.validate(valid => {
        console.info(valid)
      })
    }
  }
})
app.use(ElementPlus)
app.mount('#app')