// common dialog part
function open_common_dialog(title, url){
  dlg = $('#common_dialog');
  dlg.dialog({title: title, href: url});
  dlg.dialog('open');
}

function post_from_laws_panel(url, form_id){
  common_dialog_ajax_post(url, form_id);
  setTimeout(function(){panel_goto_page(null,'laws', '/admin/laws/list')}, 1000);
}

function post_from_news_panel(url, form_id){
  common_dialog_ajax_post(url, form_id);
  setTimeout(function(){panel_goto_page(null,'news', '/admin/news/list')}, 1000);
}


function post_from_answer_panel(url, form_id){
  common_dialog_ajax_post(url, form_id);
  setTimeout(function(){panel_goto_page(null,'question', '/admin/question/list')}, 1000);
}

function post_from_question_panel(url, form_id){
  common_dialog_ajax_post(url, form_id);
  setTimeout(function(){panel_goto_page(null,'question', '/admin/question/list')}, 1000);
}

function ajax_dialog_success(data){
  msg_html = "<div class='common_dialog_content'>"+data.message+"</div>";
  $("#common_dialog").html(msg_html);
}



function common_dialog_ajax_post(url, form_id){
  $.ajax({
     contentType: 'application/x-www-form-urlencoded; charset=UTF-8',
     url:url,
     type: 'POST',
     dataType: 'json',
     data: $('#' + form_id).serialize(),
     success: ajax_dialog_success,
     complete: function(data, status){
//       ajax_dialog_success;
     }
});

}

