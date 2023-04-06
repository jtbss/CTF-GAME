const app = Vue.createApp({
  data() {
    return {
      title: 'SSL simulator',
      show: false,
      isSending: false,
      isValidating: false,
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
          this.isSending = true

          axios.post('/send_key', {
            key: this.form1.key
          })
            .then(response => {
              c1 = response.data.data1
              c2 = response.data.data2
              // console.log(response)

              this.cipher1 = c1
              this.cipher2 = c2
              this.isSending = false
            })
            .catch(error => {
              this.isSending = false
              error_msg = error.response.data.message

              this.$notify({
                title: 'Error',
                message: error_msg || 'Wrong format of the public key',
                type: 'error',
                duration: 3000
              })
            })
        }
      })
    },
    onValidate() {
      this.$refs.form2.validate(valid => {
        if (valid) {
          this.isValidating = true

          axios.post('/validate', {
            message: this.form2.message
          })
          .then(response => {
            msg = response.data.message
            ctf = response.data.ctf
            this.isValidating = false

            if (msg === 'OK') {
              this.$alert(
                ctf,
                'Congratulation 🎉'
              )
            }
          })
          .catch(error => {
            this.isValidating = false
            error_msg = error.response?.data.message

            this.$notify({
              title: 'Error',
              message: error_msg || 'Wrong message',
              type: 'warning',
              duration: 3000
            })
          })
        }
      })
    }
  }
})
app.use(ElementPlus)
app.mount('#app')