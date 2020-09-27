<template>
  <v-app id="app">
    <v-app-bar
        app
        color="light-blue darken-3"
        dark
    >
      <v-app-bar-nav-icon class="ml-2">
        <v-icon style="font-size: 30px">mdi-semantic-web</v-icon>
      </v-app-bar-nav-icon>
      <v-toolbar-title class="font-weight-bold">JobInfo<span class="font-weight-light">Aggregation</span>
      </v-toolbar-title>
    </v-app-bar>

    <v-main>
      <v-container>
        <v-row
            class="mt-12"
            justify="space-around"
        >
          <v-fade-transition mode="out-in">
            <template v-if="error">
              <v-col
                  cols="12"
                  md="6"
                  lg="4"
                  align-self="center"
              >
                <v-card
                    height="20vh"
                    class="d-flex align-center"
                >
                  <v-row justify="center" align="center" class="pa-4 flex-column">
                    <v-card-title class="headline">{{ errorMsg }}</v-card-title>
                  </v-row>
                </v-card>
              </v-col>
            </template>
            <template v-else-if="!haveSession">
              <v-col
                  cols="12"
                  md="6"
                  lg="4"
                  align-self="center"
              >
                <v-card
                    height="50vh"
                    class="d-flex align-center"
                >
                  <v-row justify="center" align="center" class="pa-4 flex-column">
                    <v-img
                        :lazy-src="require('@/assets/placeholder.png')"
                        :src="qrcodeURL"
                        max-width="50%"
                        class="pa-8 rounded"
                    >
                      <template v-slot:placeholder>
                        <v-row
                            class="fill-height ma-0"
                            align="center"
                            justify="center"
                        >
                          <v-progress-circular
                              indeterminate
                              color="grey lighten-5"
                          ></v-progress-circular>
                        </v-row>
                      </template>
                    </v-img>
                    <v-card-subtitle
                        class="heading qrcode-title"
                    >
                      请使用学习通扫描二维码
                    </v-card-subtitle>
                  </v-row>
                </v-card>
              </v-col>
            </template>
            <template v-else-if="haveSession&&!haveData">
              <v-col
                  cols="12"
                  md="4"
                  lg="3"
                  v-for="(i) in 4"
                  :key="i"
              >
                <v-skeleton-loader
                    type="card"
                ></v-skeleton-loader>
              </v-col>
            </template>
            <template v-else>
              <v-col
                  cols="12"
                  md="4"
                  lg="'3"
              >
                <v-card>
                  <v-img
                      src="https://picsum.photos/600/200"
                      contain
                  />
                  <v-card-title
                      class="headline"
                  >
                    Top western road trips
                  </v-card-title>

                  <v-card-subtitle
                      class="heading pt-2"
                  >
                <span
                    class="course-name"
                >
                  课程名
                </span>
                    <span class="by-name d-inline-block">&emsp;</span>
                    <span
                        class="font-weight-light grey--text teacher-name"
                    >
                  教师名asddddddddddddddddddddddddddddddddddddddd
                </span>
                  </v-card-subtitle>
                  <v-card-actions>
                    <v-spacer/>
                    <v-btn
                        text
                        color="orange lighten-2"
                    >
                      DO IT!
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </v-col>
            </template>
          </v-fade-transition>
        </v-row>
      </v-container>
    </v-main>
    <v-footer
        color="light-blue darken-3"
        app
    >
      <span class="white--text">&copy; {{ new Date().getFullYear() }}</span>
    </v-footer>
    <v-snackbar
        v-model="snackbarBool"
        :color="snackbarColor"
        top
        dark
    >
      {{ snackbarMessage }}
      <template v-slot:action="{ attrs }">
        <v-btn
            dark
            text
            v-bind="attrs"
            @click="snackbarBool = false"
        >
          关闭
        </v-btn>
      </template>
    </v-snackbar>
  </v-app>
</template>

<script>
import axios from 'axios'
import ls from 'localStorage'

export default {
  name: "App",
  data() {
    return {
      error: false,
      errorMsg: '',
      haveSession: false,
      workData: [],
      haveData: false,
      qrcodeURL: '',
      snackbarBool: false,
      snackbarMessage: '',
      snackbarColor: '',
      enc: '',
      uuid: '',
      session: {}
    }
  },
  mounted() {
    if (!this.checkRunning()) {
      this.error = true
      this.errorMsg = '后端在启动中，请10秒后再试。'
      return 0
    } else {
      if (!this.checkServerXXTConnect()) {
        this.error = true
        this.errorMsg = '后端服务器无法连接学习通，请联系管理员'
        return 0
      }
    }
    this.haveSession = this.checkSession()
    if (this.haveSession) {
      this.getWorkData()
    } else {
      this.getLoginData()
      let trytime2 = 0
      while (trytime2 < 50) {
        if (trytime2 === 40) {
          this.getLoginData()
        }
        let url = this.$apiurl + '/login/auth'
        axios.post(url, {
          'valid': {
            'enc': this.enc,
            'uuid': this.uuid,
            'session': this.session
          }
        }).then((resp) => {
          if (!resp.data['status']) {
            this.sleep(3000).then(() => {
              trytime2++
            })
          } else {
            ls.setItem('session', JSON.stringify(resp.data['session']))
            this.showSnackbar(['登陆成功', 'success'])
            trytime2 = 100
          }
        })
      }
      this.getWorkData()
    }
  },
  methods: {
    sleep: function (time) {
      return new Promise((resolve) => setTimeout(resolve, time))
    },
    showSnackbar: function (arg) {
      this.snackbarMessage = arg[0]
      this.snackbarColor = arg[1]
      this.snackbarBool = true
    },
    getSession: function () {
      return {'session': JSON.parse(ls.getItem('session'))}
    },
    checkSession: function () {
      if (ls.length === 0) {
        return false
      } else {
        let url = this.$apiurl + '/login/verifyCookies'
        axios.post(url, this.getSession()).then(function (resp) {
          return resp
        })
      }
    },
    checkRunning: function () {
      let url = this.$apiurl + '/checkRunning'
      axios.get(url, {timeout: 3000}).then(function () {
        return true
      }).catch(function () {
        return false
      })
    },
    checkServerXXTConnect: function () {
      let url = this.$apiurl + '/checkXXTConnect'
      axios.get(url).then(function (resp) {
        return resp.data;
      })
    },
    getWorkData: function () {
      let url = this.$apiurl + '/info'
      let that = this
      axios.post(url, this.getSession()).then(function (resp) {
        that.workData = resp.data['workInfo']
        that.haveData = true
        that.showSnackbar(['查询成功', 'success'])
      })
    },
    getLoginData: function () {
      let url = this.$apiurl + '/login/code'
      let that = this
      axios.get(url).then(function (resp) {
        that.qrcodeURL = resp.data['pic']
        that.enc = resp.data['valid']['enc']
        that.uuid = resp.data['valid']['uuid']
        that.session = resp.data['valid']['session']
      })
    }
  }
}
</script>

<style>
.teacher-name, .course-name {
  display: inline-block;
  max-width: 6em;
  white-space: nowrap;
  text-overflow: ellipsis;
  word-break: break-all;
  overflow: hidden;
}

.course-name {
  max-width: 16em !important;
}

.by-name {
  display: inline-block;
}

.qrcode-title {
  font-size: 20px !important;
}
</style>