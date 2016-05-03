export class CoderBotSrv {
  static getCurrentUser () {
    var promise = new Promise(function (resolve, reject) {
      $.get('/api/coderbot/1.0/user', function (data) {
        resolve(data.user_data)
      }, 'json')
    })
    return promise
  }

  static getOwnBotList () {
    var promise = new Promise(function (resolve, reject) {
      $.get('/api/coderbot/1.0/user/bots', function (data) {
        resolve(data.bot_list)
      }, 'json')
    })
    return promise
  }

  static getBotDetail (bot_id) {
    var promise = new Promise(function (resolve, reject) {
      $.get('/api/coderbot/1.0/user/bots/' + bot_id, function (data) {
        resolve(data.bot_data)
      }, 'json')
    })
    return promise
  }

  static setBotDetail (bot_id, bot_data) {
    var data = JSON.strigify(bot_data)
    var promise = new Promise(function (resolve, reject) {
      $.ajax({url: '/api/coderbot/1.0/user/bots/' + bot_id, type: 'PUT', data: data, success: function (data) {
        resolve(data.bot_data)
      }, dataType: 'json'})
    })
    return promise
  }

  static getPrivateProgramList () {
    var data = {'status': 1}
    data = JSON.stringify(data)
    var promise = new Promise(function (resolve, reject) {
      $.get('/api/coderbot/1.0/user/programs', data, function (data) {
        resolve(data.program_list)
      }, 'json')
    })
    return promise
  }

  static findPrograms (status, tags) {
    var data = {'tags': tags, 'status': status}
    data = JSON.stringify(data)
    var promise = new Promise(function (resolve, reject) {
      $.post('/api/coderbot/1.0/user/programs', data, function (data) {
        resolve(data.program_list)
      }, 'json')
    })
    return promise
  }

  static getProgramDetail (prog_id) {
    var promise = new Promise(function (resolve, reject) {
      $.get('/api/coderbot/1.0/user/programs/' + prog_id, function (data) {
        resolve(data.program_data)
      }, 'json')
    })
    return promise
  }

  static setProgramDetail (prog_id, program) {
    var data = program
    var promise = new Promise(function (resolve, reject) {
      $.post('/api/coderbot/1.0/user/program/' + prog_id, data, function (data) {
        resolve(data.program_data)
      }, 'json')
    })
    return promise
  }

  static getEvents () {
    var promise = new Promise(function (resolve, reject) {
      $.get('/api/coderbot/1.0/user/events', function (data) {
        console.log(data)
        resolve(data.events)
      }, 'json')
    })
    return promise
  }
}

CoderBotSrv.PROGRAM_STATUS_PRIVATE = 1
CoderBotSrv.PROGRAM_STATUS_PUBLIC = 10
CoderBotSrv.PROGRAM_STATUS_DELETED = 99
