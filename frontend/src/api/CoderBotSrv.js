export class CoderBotSrv {
  static getCurrentUser () {
    var promise = new Promise(function (resolve, reject) {
      $.get('/api/coderbot/1.0/user/current', function (data) {
        resolve(data.user_data)
      }, 'json')
    })
    return promise
  }

  static getOwnBotList () {
    var promise = new Promise(function (resolve, reject) {
      $.get('/api/coderbot/1.0/bot/list', function (data) {
        resolve(data.bot_list)
      }, 'json')
    })
    return promise
  }

  static getOwnProgramList () {
    var promise = new Promise(function (resolve, reject) {
      $.get('/api/coderbot/1.0/program/list', function (data) {
        resolve(data.program_list)
      }, 'json')
    })
    return promise
  }
}
