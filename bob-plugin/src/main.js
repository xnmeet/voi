var config = require('./config.js');
var utils = require('./utils.js');

function supportLanguages() {
  return config.supportedLanguages.map(([standardLang]) => standardLang);
}

function tts(query, completion) {
  const targetLanguage = utils.langMap.get(query.lang);
  if (!targetLanguage) {
    const err = new Error(`不支持 ${query.lang} 语种`);
    throw err;
  }
  const originText = query.text;

  try {
    $http.request({
      method: 'POST',
      url: $option.baseUrl,
      header: {
        'Content-Type': 'application/json'
      },
      body: {
        text: originText,
        voice: $option.voice,
        speed: 1,
        stream: false,
        format: 'base64'
      },
      handler: function (resp) {
        var rawData = resp.data.audio_data;
        completion({
          result: {
            type: 'base64',
            value: rawData,
            raw: rawData
          }
        });
      }
    });
  } catch (e) {
    $log.error(e);
  }
}

exports.supportLanguages = supportLanguages;
exports.tts = tts;
