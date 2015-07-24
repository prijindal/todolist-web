$(document).foundation({
  accordion: {
    content_class: 'details'
    }
});

$("#editProject").on('click', function() {
  if($(this).hasClass("edit")) {
    var content = $(this).siblings('.description').html()
    content = content.trim()
    $(this).siblings('.description').html('<textarea>'+content+'</textarea>')
    $(this).removeClass("edit").addClass("done-edit").html("Done")
  }
  else {
    var content = $(this).siblings('.description').children('textarea').val()
    content = content.trim()
    console.log(content);
    $(this).siblings('.description').html(content)
    $(this).removeClass("done-edit").addClass("edit").html("Edit This")
    var project = $(this).data("project")
  	var title = $(this).data("title")
  	var url = '/'+project+'/edit'
  	$.ajax({
  		url:url,
      type:'POST',
      data:{newContent:content},
  		success:function(data) {
        console.log('done');
  		},
      error:function(error) {
        console.error(error);
      }
  	})
  }
})

$("#editThis").on('click', function() {
  if($(this).hasClass("edit")) {
    var content = $(this).siblings('.content').children('.text-content').html()
    content = content.trim()
    $(this).siblings('.content').children('.text-content').html('<textarea>'+content+'</textarea>')
    $(this).removeClass("edit").addClass("done-edit").html("Done")
  }
  else {
    var content = $(this).siblings('.content').children('.text-content').children('textarea').val()
    content = content.trim()
    console.log(content);
    $(this).siblings('.content').children('.text-content').html(content)
    $(this).removeClass("done-edit").addClass("edit").html("Edit This")
    var project = $(this).data("project")
  	var title = $(this).data("title")
  	var url = '/'+project+'/'+title+'/edit'
  	$.ajax({
  		url:url,
      type:'POST',
      data:{newContent:content},
  		success:function(data) {
        console.log('done');
  		},
      error:function(error) {
        console.error(error);
      }
  	})
  }
})

$("#deleteThis").on('click',function() {
	$("#deleteModal #yes").attr("data-href",$(this).attr("data-href"))
	$("#deleteModal #yes").attr("data-target","task")
})

$("#deleteProject").on('click',function() {
	$("#deleteModal #yes").attr("data-href",$(this).attr("data-href"))
	$("#deleteModal #yes").attr("data-target","project")
})

$("#deleteModal #yes").on('click',function() {
	var url = $(this).data("href")
	var target = $("#deleteModal #yes").attr("data-target")
	console.log(url,target)
	$.ajax({
		url:url,
		success:function(data) {
			if (target=="task") {
				window.location.reload()
			}
			else {
				window.location.href="/"
			}
		}
	})
})

$(".setCompleted").on('click',function() {
	var project = $(this).data("project")
	var title = $(this).data("title")
	var url = '/'+project+'/'+title+'/complete'
	console.log(url)
	$.ajax({
		url:url,
		success:function(data) {
			window.location.reload()
		}
	})
})
$(".setRemaining").on('click',function() {
	var project = $(this).data("project")
	var title = $(this).data("title")
	var url = '/'+project+'/'+title+'/remain'
	console.log(url)
	$.ajax({
		url:url,
		success:function(data) {
			window.location.reload()
		}
	})
})
