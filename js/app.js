$(document).foundation({
  accordion: {
    content_class: 'details'
    }
});


$(".editProject").on('click', function() {
  if($(this).hasClass("edit")) {
    var content = $(this).siblings('.description').html()
    content = content.trim()
    $(this).siblings('.description').html('<textarea>'+content+'</textarea>')
    $(this).removeClass("edit").addClass("done-edit").html("Done")
  }
  else {
    var content = $(this).siblings('.description').children('textarea').val()
    content = content.trim()

    $(this).siblings('.description').html(content)
    $(this).removeClass("done-edit").addClass("edit").html("Edit This")
    var project = $(this).data("project")

  	var url = '/'+project+'/edit'
  	$.ajax({
  		url:url,
      type:'PUT',
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


$(".editThis").on('click', function() {
  if($(this).hasClass("edit")) {
    var content = $(this).siblings('.content').children('.text-content').html()
    $(this).siblings('.content').children('.small-text').children('input').removeAttr("disabled")
    content = content.trim()
    $(this).siblings('.content').children('.text-content').html('<textarea>'+content+'</textarea>')
    $(this).removeClass("edit").addClass("done-edit").html("Done")
  }
  else {
    var content = $(this).siblings('.content').children('.text-content').children('textarea').val()
    $(this).siblings('.content').children('.small-text').children('input').attr("disabled","disabled")
    var date = $(this).siblings('.content').children('.small-text').children('input').val()
    content = content.trim()
    console.log(content);
    $(this).siblings('.content').children('.text-content').html(content)
    $(this).removeClass("done-edit").addClass("edit").html("Edit This")
    var project = $(this).data("project")
  	var title = $(this).data("title")
  	var url = '/'+project+'/'+title+'/edit'
  	$.ajax({
  		url:url,
      type:'PUT',
      data:{newContent:content,newDate:date},
  		success:function(data) {
        console.log('done');
  		},
      error:function(error) {
        console.error(error);
      }
  	})
  }
})

var deleteDetails;
function setDelete(project, task) {
    deleteDetails = {
        'project':project,
        'task': task
        }
}

function setDeleteProject(project) {
    deleteDetails = {
        'project':project
        };
}

$("#deleteModal #yes").on('click',function() {
    console.log(deleteDetails);
    var url;
    if (deleteDetails['task']) {
        url = url = '/'+deleteDetails['project']+'/'+deleteDetails['task']+'/delete'
    }
    else {
        url = url = '/'+deleteDetails['project']+'/delete'
    }
	console.log(url)
	$.ajax({
		url:url,
        type:'DELETE',
		success:function(data) {
            if(deleteDetails['task']) {
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
        type:'PUT',
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
        type:'PUT',
		success:function(data) {
			window.location.reload()
		}
	})
})
