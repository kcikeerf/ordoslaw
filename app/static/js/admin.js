function panel_goto_page(n, panel,url){

  var total_pages = parseInt($("#admin_"+panel+"_total_pages").val());

  var current_page = parseInt($("#admin_"+panel+"_pagination_form input[name='page']").val());
  if(typeof n == 'undefined' || n == null || isNaN(n)){n=current_page;}
  if( n && n >0 && n <=total_pages){
      $("admin_"+panel+"_pagination_form input").val(n);
      $("#admin_"+panel).panel('clear');
      $("#admin_"+panel).panel({href: url + "?page=" + n});
      return true;
  } else {
    return false;
  }
}


function onAdminPanelListLoad(panel, url){
//console.info(panel);
var total_pages = parseInt($("#admin_"+panel+"_total_pages").val());

$("#admin_"+panel+"_pagination_form input[name='page']").on("keypress",function(e){
  var current_page = parseInt($("#admin_"+panel+"_pagination_form input").val());
  if(e.keyCode == '13'){
    return panel_goto_page(current_page, panel,url);
  }
});

$("#admin_"+panel+"_first").on("click", function(){
  var current_page=parseInt($("#admin_"+panel+"_pagination_form input[name='page']").val());
  if(total_pages > 1 ){
    panel_goto_page(1, panel,url);
  }
});

$("#admin_"+panel+"_forward").on("click", function(){
  var current_page=parseInt($("#admin_"+panel+"_pagination_form input[name='page']").val());
  var target = current_page - 1;
  //if(current_page > 0 && current_page <= total_pages){
    panel_goto_page(target, panel,url);
  //}
});

$("#admin_"+panel+"_backward").on("click", function(){
  var current_page=parseInt($("#admin_"+panel+"_pagination_form input[name='page']").val());
  var target = current_page + 1;
  //if(target > 0 && target <= total_pages){
    panel_goto_page(target,  panel,url);
  //}
});

$("#admin_"+panel+"_last").on("click", function(){
  var current_page=parseInt($("#admin_"+panel+"_pagination_form input[name='page']").val());
  if(current_page != total_pages && total_pages > 1){
    panel_goto_page(total_pages, panel,url);
  }
});

}
