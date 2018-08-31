# Delete addons
curl -X DELETE -H "Content-Type: application/json" -d '{
  "setting_type":"call_to_actions",
  "thread_state":"new_thread"
}' "https://graph.facebook.com/v2.6/me/thread_settings?access_token=${WORKPLACE_ACCESS_TOKEN}"

# Button Get Started

curl -X POST -H "Content-Type: application/json" -d '{ 
  "get_started":{
    "payload":"START"
  }
}' "https://graph.facebook.com/v2.6/me/messenger_profile?access_token=${WORKPLACE_ACCESS_TOKEN}"

# Nested persisten menu
# https://www.piliapp.com/facebook-symbols/chat/

curl -X POST -H "Content-Type: application/json" -d '{
  "persistent_menu":[
    {
      "locale":"default",
      "composer_input_disabled": false,
      "call_to_actions":[
        {
          "title":"📔 Informacion",
          "type":"nested",
          "call_to_actions":[
            {
              "title":"🏢 Positiva",
              "type":"web_url",
              "url":"https://www.lapositiva.com.pe/wps/portal/corporativo/home"
            },
            {
              "title":"📄 Terminos y condiciones",
              "type":"web_url",
              "url":"https://www.lapositiva.com.pe/wps/portal/corporativo/home"
            }
          ]
        },
        {
          "type":"postback",
          "title":"🔎 Nueva Consulta",
          "payload":"START"
        },
        {
          "type":"postback",
          "title":"📑 Ver Tutorial",
          "payload":"SHOW_TUTORIAL"
        },
      ]
    }
  ]
}' "https://graph.facebook.com/v2.6/me/messenger_profile?access_token=${WORKPLACE_ACCESS_TOKEN}"

