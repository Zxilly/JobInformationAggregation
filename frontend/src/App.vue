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
            class="mt-6"
            justify="start"
        >
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
                  lg="3"
                  class="mx-auto"
                  align-self="center"
              >
                <v-card
                    height="50vh"
                    class="d-flex align-center"
                >
                  <v-row justify="center" align="center" class="pa-4 flex-column">
                    <v-img
                        :src="qrcodeURL"
                        max-width="50%"
                        class="pa-8 rounded"
                    >
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
            <template v-else-if="!haveData">
                <v-col
                    cols="12"
                    md="6"
                    lg="4"
                    v-for="(i) in 3"
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
                  md="6"
                  lg="4"
                  class="pb-4"
                  v-for="(oneWorkData,i) in workData"
                  :key="i"
              >
                <v-card>
                  <v-img
                      :src="'https://picsum.photos/seed/'+(oneWorkData['workName'])+'/600/200'"
                      :lazy-src="require('@/assets/600x200.png')"
                      contain
                  />
                  <v-card-title
                      class="headline"
                  >
                    {{oneWorkData['workName']}}
                  </v-card-title>

                  <v-card-subtitle
                      class="heading pt-2"
                  >
                <span
                    class="course-name"
                >
                  {{ oneWorkData['courseName'] }}
                </span>
                    <span class="by-name d-inline-block">&emsp;</span>
                    <span
                        class="font-weight-light grey--text teacher-name"
                    >
                  {{oneWorkData['teacherName']}}
                </span>
                  </v-card-subtitle>
                  <v-divider/>
                  <v-card-actions>
                    <v-chip
                        class="ml-2"
                    >
                      <v-icon>mdi-alarm</v-icon>&nbsp;
                      {{oneWorkData['workTime']}}
                    </v-chip>
                    <v-spacer/>
                    <v-btn
                        text
                        color="orange lighten-2"
                        style="font-size: 1rem"
                        class="mr-2"
                        @click="goWork(oneWorkData['workURL'])"
                    >
                      DO IT!
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </v-col>
            </template>
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
      session: {},
      tryTime:0,
    }
  },
  mounted() {
    this.checkRunning()
  },
  methods: {
    sleep: function (time) {
      return new Promise((resolve) => setTimeout(resolve, time))
    },
    goWork: function (url) {
      window.open(url,'_blank')
    }
    ,
    showSnackbar: function (arg) {
      this.snackbarMessage = arg[0]
      this.snackbarColor = arg[1]
      this.snackbarBool = true
    },
    getSession: function () {
      return {'session': JSON.parse(ls.getItem('session'))}
    },
    checkSession: function () {
      let that=this
      if (ls.getItem('jia')===null) {
        that.getLoginData()
      } else {
        let url = this.$apiurl + '/login/verifyCookies'
        axios.post(url, this.getSession()).then(function (resp) {
          if(resp.data){
            that.haveSession = true
            that.getWorkData()
          } else {
            that.getLoginData()
          }
        })
      }
    },
    checkAuth: function () {
      let url = this.$apiurl + '/login/auth'
      let that = this
      axios.post(url, {
        'valid': {
          'enc': this.enc,
          'uuid': this.uuid,
          'session': this.session
        }
      }).then(function (resp) {
        if(!resp.data['status']){
          that.sleep(2000).then(()=>{
            that.tryTime++
            if(that.tryTime>40){
              that.getLoginData()
            } else {
              that.sleep(2000).then(()=>{
                that.checkAuth()
              })
            }
          })
        } else {
          ls.setItem('session', JSON.stringify(resp.data['session']))
          ls.setItem('jia','1')
          that.showSnackbar(['登陆成功', 'success'])
          that.haveSession = true
          that.getWorkData()
        }
      })
    },
    checkRunning: function () {
      let that = this
      let url = this.$apiurl + '/checkRunning'
      axios.get(url, {timeout: 2000}).then(function () {
        that.checkServerXXTConnect()
      }).catch(function () {
        that.error = true
        that.errorMsg = '后端在启动中，请10秒后再试。'
      })
    },
    checkServerXXTConnect: function () {
      let that = this
      let url = this.$apiurl + '/checkXXTConnect'
      axios.get(url).then(function (resp) {
        if(!resp.data){
          that.error = true
          that.errorMsg = '后端服务器无法连接学习通，请联系管理员'
        } else {
          that.checkSession()
        }
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
        that.checkAuth()
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