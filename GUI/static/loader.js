var channels = {
   html: {
      socket: null,

      requests: 5,

      start: function() {
         channels.html.socket = new WebSocket("ws://" + location.host + "/html");
         channels.html.socket.onmessage = function(event) {
            if (channels.html.requests > 0) {
               channels.html.requests--;
            } else if (channels.html.requests == 0) {
               return;
            }
            console.log(event);
            $('#global').html(event.data);
         }
      },

      end: function() {
         channels.html.socket.close()
      }
   },

   data: {
      socket: null,

      request: -1,

      start: function() {
         channels.data.socket = new WebSocket("ws://" + location.host + "/data");
         channels.data.socket.onmessage = function(event) {
            if (channels.html.requests > 0) {
               channels.html.requests--;
            } else if (channels.html.requests == 0) {
               return;
            }
            console.log(event)
         }
      },

      end: function() {
         channels.data.socket.close()
      }
   }
};
