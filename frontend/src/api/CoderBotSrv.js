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

  static getBotDetail (bot_id) {
    var promise = new Promise(function (resolve, reject) {
      $.get('/api/coderbot/1.0/bot/' + bot_id, function (data) {
        resolve(data.bot_data)
      }, 'json')
    })
    return promise
  }

  static setBotDetail (bot_id, bot_data) {
    var data = bot_data
    var promise = new Promise(function (resolve, reject) {
      $.post('/api/coderbot/1.0/bot/' + bot_id, data, function (data) {
        resolve(data.bot_data)
      }, 'json')
    })
    return promise
  }

  static getPrivateProgramList () {
    var promise = new Promise(function (resolve, reject) {
      $.get('/api/coderbot/1.0/program/list', function (data) {
        resolve(data.program_list)
      }, 'json')
    })
    return promise
  }

  static findPublicProgramList (name, tags) {
    var data = {'tags': tags}
    var promise = new Promise(function (resolve, reject) {
      $.post('/api/coderbot/1.0/program/list', data, function (data) {
        resolve(data.program_list)
      }, 'json')
    })
    return promise
  }

  static getProgramDetail (prog_id) {
    var promise = new Promise(function (resolve, reject) {
      $.get('/api/coderbot/1.0/program/' + prog_id, function (data) {
        resolve(data.program_data)
      }, 'json')
    })
    return promise
  }

  static setProgramDetail (prog_id, program) {
    var data = program
    var promise = new Promise(function (resolve, reject) {
      $.post('/api/coderbot/1.0/program/' + prog_id, data, function (data) {
        resolve(data.program_data)
      }, 'json')
    })
    return promise
  }
}
