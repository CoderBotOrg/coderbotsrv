export class CoderBotSrv {
  static getOwnBotList () {
    var promise = new Promise(function (resolve, reject) {
      $.get('/api/coderbot/v1.0/bot/list', function (data) {
        resolve(data.bot_list)
      }, 'json')
    })
    return promise
  }

  static getOwnProgramList () {
    var promise = new Promise(function (resolve, reject) {
      $.get('/api/coderbot/v1.0/program/list', function (data) {
        resolve(data.program_list)
      }, 'json')
    })
    return promise
  }
}
