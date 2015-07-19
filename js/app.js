$(document).foundation({
  accordion: {
    content_class: 'details'
    }
});

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