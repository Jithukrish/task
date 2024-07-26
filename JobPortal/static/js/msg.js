

// let value_message = $('#message');
// let message_body = $('.msg_card_body');
// let send_message_form = $('.messageForm');
// const USER_ID = $('#logged-in-user').val();

// let loc = window.location;
// let wsStart = 'ws://';

// if (loc.protocol === 'https:') {
//     wsStart = 'wss://';
// }

// let endpoint = wsStart + loc.host + loc.pathname;
// var socket = new WebSocket(endpoint);

// socket.onopen = function(e) {
//     console.log('open', e);
//     send_message_form.on('submit', function(e) {
//         e.preventDefault();
//         let message = value_message.val();
//         let send_to = get_active_other_user_id();
//         let data = {
//             'message': message,
//             'sent_by': USER_ID,
//             'send_to': send_to
//         };
//         data = JSON.stringify(data);
//         socket.send(data);
//         $(this)[0].reset();
//     });
// };

// socket.onmessage = function(e) {
//     console.log('message', e);
//     let data = JSON.parse(e.data);
//     let message = data['message'];
//     let sent_by_id = data['sent_by'];
//     let thread_id = data['thread_id'];
//     newMessage(message, sent_by_id, thread_id);
// };

// socket.onerror = function(e) {
//     console.log('error', e);
// };

// socket.onclose = function(e) {
//     console.log('close', e);
// };

// function newMessage(message, sent_by_id, thread_id) {
//     if ($.trim(message) === '') {
//         return false;
//     }
//     let message_element;
//     let chat_id = 'chat_' + thread_id;
//     if (sent_by_id == USER_ID) {
//         message_element = `
//             <li class="me">
//                 <div class="entete">
//                     <h3>10:12AM, Today</h3>
//                     <h2>Alen</h3>
//                     <span class="status blue"></span>
//                 </div>
//                 <div class="triangle"></div>
//                 <div class="message">
//                     ${message}
//                 </div>
//             </li>
//         `;
//     } else {
//         message_element = `
//             <li class="you">
//                 <div class="entete">
//                     <span class="status green"></span>
//                     <h2>Vincent</h2>
//                     <h3>10:12AM, Today</h3>
//                 </div>
//                 <div class="triangle"></div>
//                 <div class="message">
//                     ${message}
//                 </div>
//             </li>
//         `;
//     }

//     let message_body = $('.messages-wrapper[chat-id="' + chat_id + '"] .msg_card_body');
//     message_body.append($(message_element));
//     message_body.animate({
//         scrollTop: $(document).height()
//     }, 100);
//     value_message.val(null);
// }

// $('.contact-li').on('click', function() {
//     $('.contacts .active').removeClass('active');
//     $(this).addClass('active');

//     let chat_id = $(this).attr('chat-id');
//     $('.messages-wrapper.is_active').removeClass('is_active');
//     $('.messages-wrapper[chat-id="' + chat_id + '"]').addClass('is_active');
// });

// function get_active_other_user_id() {
//     let other_user_id = $('.messages-wrapper.is_active').attr('other-user-id');
//     other_user_id = $.trim(other_user_id);
//     return other_user_id;
// }

// function get_active_thread_id() {
//     let chat_id = $('.messages-wrapper.is_active').attr('chat-id');
//     let thread_id = chat_id.replace('chat_', '');
//     return thread_id;
// }

$(document).ready(function() {
    let value_message = $('#message');
    let message_body = $('.msg_card_body');
    let send_message_form = $('#messageForm');
    const USER_ID = $('#logged-in-user').val();

    let loc = window.location;
    let wsStart = loc.protocol === 'https:' ? 'wss://' : 'ws://';
    let endpoint = wsStart + loc.host + '/ws/chat_router/';

    var socket = new WebSocket(endpoint);

    socket.onopen = function(e) {
        console.log('WebSocket connection opened:', e);
        send_message_form.on('submit', function(e) {
            e.preventDefault();
            let message = value_message.val();
            if ($.trim(message) === '') {
                return; 
            }
            let send_to = get_active_other_user_id();
            if (!send_to) {
                console.error('No active user selected.');
                return; 
            }
            let data = {
                'message': message,
                'sent_by': USER_ID,
                'send_to': send_to
            };
            socket.send(JSON.stringify(data));
            $(this)[0].reset();
        });
    };

    socket.onmessage = function(e) {
        console.log('Message received:', e);
        let data = JSON.parse(e.data);
        let message = data['message'];
        let sent_by_id = data['sent_by'];
        let thread_id = data['thread_id'];
        newMessage(message, sent_by_id, thread_id);
    };

    socket.onerror = function(e) {
        console.error('WebSocket error:', e);
    };

    socket.onclose = function(e) {
        console.log('WebSocket connection closed:', e);
        if (!e.wasClean) {
            console.warn('WebSocket connection closed unexpectedly:', e.reason);
        } else {
            console.info('WebSocket connection closed cleanly');
        }
    };

    function newMessage(message, sent_by_id, thread_id) {
        if ($.trim(message) === '') {
            return; 
        }
        let message_element;
        let chat_id = 'chat_' + thread_id;
        let timestamp = new Date().toLocaleTimeString(); 

        if (sent_by_id == USER_ID) {
            message_element = `
                <li class="me">
                    <div class="entete">
                        <h3>${timestamp}</h3>
                        <h2>${$('#logged-in-user').data('username')}</h2>
                        <span class="status blue"></span>
                    </div>
                    <div class="triangle"></div>
                    <div class="message">${message}</div>
                </li>
            `;
        } else {
            message_element = `
                <li class="you">
                    <div class="entete">
                        <span class="status green"></span>
                        <h2>${get_username_from_id(sent_by_id)}</h2>
                        <h3>${timestamp}</h3>
                    </div>
                    <div class="triangle"></div>
                    <div class="message">${message}</div>
                </li>
            `;
        }

    let message_body = $('.messages-wrapper[chat-id="' + chat_id + '"] .msg_card_body');
    message_body.append($(message_element));
    message_body.animate({ scrollTop: message_body[0].scrollHeight }, 100);
    value_message.val(null);
    }

    $('.contact-li').on('click', function() {
        $('.contacts .active').removeClass('active');
        $(this).addClass('active');

        let chat_id = $(this).attr('chat-id');
        $('.messages-wrapper.is_active').removeClass('is_active');
        $('.messages-wrapper[chat-id="' + chat_id + '"]').addClass('is_active');
    });

    function get_active_other_user_id() {
        return $.trim($('.messages-wrapper.is_active').attr('other-user-id'));
    }

    function get_active_thread_id() {
        let chat_id = $('.messages-wrapper.is_active').attr('chat-id');
        return chat_id.replace('chat_', '');
    }

    function get_username_from_id(user_id) {
        return 'Username'; 
    }
});


  
       
    

    
            

   
                       
                 
   


   
