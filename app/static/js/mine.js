
$(document).ready(function(){
var total_pages = parseInt($("#publish_list_total_pages").val());

function goto_publish_list_page(n){
  var current_page = $("#publish_list_pagination_form input").val();
  if(n &&  n >0 && n <= parseInt(total_pages)){
    $("#publish_list_pagination_form input").val(n);
    $("#publish_list_pagination_form").submit();
    return true;
  } else {
    return false;
  }
}

$("#publish_list_pagination_form input[name='page']").on("keypress", function(e){
  var current_page = parseInt($("#publish_list_pagination_form input").val());
  if(e.keyCode == '13'){
    return goto_publish_list_page(current_page);
  }
});

$("#publish_list_first").on("click", function(){
  if(total_pages > 1 ){
    goto_publish_list_page(1);
  }
});

$("#publish_list_forward").on("click", function(){
  var current_page=parseInt($("#publish_list_pagination_form input[name='page']").val());
  var target = current_page - 1;
  if(current_page > 0 && current_page <= total_pages){
    goto_publish_list_page(target);}});

$("#publish_list_backward").on("click", function(){
  var current_page=parseInt($("#publish_list_pagination_form input[name='page']").val());
  var target = current_page + 1;
  if(target > 0 && target <= total_pages){
    goto_publish_list_page(target);}});

$("#publish_list_last").on("click", function(){
  var current_page=parseInt($("#publish_list_pagination_form input[name='page']").val());
  if(current_page != total_pages && total_pages > 1){
    goto_publish_list_page(total_pages);
  }
});

$('#current_url_qrcode').qrcode({
  "size": 100,
  "text": window.location.href
});

});

