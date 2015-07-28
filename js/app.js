$(document).foundation({
  accordion: {
    content_class: 'details'
    }
});

$('.task-button').each(function( index ) {
    task_checker(this)
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


$(".editThis").on('click', function() {
    var $selector = $(this).siblings('.content')
  if($(this).hasClass("edit")) {
    var content = $selector.children('.text-content').html()
    $selector.children('.small-text').children('input').removeAttr("disabled")
    content = content.trim()
    $selector.children('.text-content').html('<textarea>'+content+'</textarea>')
    $(this).removeClass("edit").addClass("done-edit").html("Done")
  }
  else {
    var content = $selector.children('.text-content').children('textarea').val()
    $selector.children('.small-text').children('input').attr("disabled","disabled")
    var date = $selector.children('.small-text').children('input').val()
    content = content.trim()
    console.log(content);
    $selector.children('.text-content').html(content)
    $(this).removeClass("done-edit").addClass("edit").html("Edit This")
    var project = $(this).data("project")
  	var title = $(this).data("title")
  	var url = '/'+project+'/'+title+'/edit'
  	$.ajax({
  		url:url,
      type:'POST',
      data:{newContent:content,newDate:date},
  		success:function(data) {
        console.log('done');
        $selector.parent().siblings('.task-button').each(function() {
            task_checker(this)
        })
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
		success:function(data) {
            if (deleteDetails['task']) {
                window.location.reload()
            }
            else {
                window.location.href='/'
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

function task_checker(thisObject) {
    var task_date = $(thisObject).siblings('.details').find('.content p input').val()
    var task = new Date(task_date);
    task.setHours(23)
    task.setMinutes(59)
    task.setSeconds(59)
    var now = new Date();
    console.log(task, now, task_date);
    var diff = task - now;
    if (diff < 0) {
        $(thisObject).parent().addClass('warning')
    }
}
