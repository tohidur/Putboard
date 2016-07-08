$(document).ready(function(){
	var id = 0;
	$('#formBoard').validate({
		rules: {
			title: "required"
		},
		messages: {
			title: 'Please enter a Board Name',
		}
	})

	
	$('#formLink').validate({
		rules: {
			link: {
				required: true,
			}
		},
		messages: {
			link: {
				required: 'Url field is required',
			}
		},
		submitHandler: function(form){
			id = id+1;
			var temp = id;
		 	$('#addLink').modal('hide');
		 	var link = $('#formLink #id_link').val();
		 	var title = $('#formLink #id_title').val();
		 	var tags = [];
		 	tags = $('#formLink #id_tags').val();
		 	console.log(tags);
		 	var domain;
		 	if (link.indexOf("://") > -1) {
		 	    domain = link.split('/')[2];
		 	    if (domain.startsWith('www')){
		 	    	domain = domain.substring(4);
		 	    }
		 	}
		 	else {
		 	    domain = link.split('/')[0];
		 	}
		 	domain = domain.split(':')[0];
		 	console.log(domain);
	        var formData = {
	            'title': title,
	            'link': link,
	            'tags': tags,
	        };
	        console.log(formData);
	        $.ajax({
	            type: 'POST',
	            url: '/'+slug+'/add',
	            data: formData,
	            beforeSend: function(){
	            	if (title != null) {
	            		title = domain;
	            	}
					var task = '<div id="img-'+temp+'" class="col-md-3 col-sm-6 col-xs-12">'+'<a href="'+link+'" target="_blank">'+
						'<div class="card"><div class="img-container"><img src="'+wait+'"></div>'+'<div class="details"><div class="link-title">'+title+'</div></div><div class="hosts">'+
						'<span><!--- Host Favicon --> <img src="http://'+domain+'/favicon.ico"> </span><span class="host-name">'+
						domain+'</span><span class="pull-right tag"> <i class="fa fa-tag mar-r-5" aria-hidden="true"></i> Startup </span>'+
						'</div><div class="clearfix"></div></div></a></div>'
					console.log(task)
					$('.card-lists').prepend(task);
	            },
	            success: function (data) {
	                console.log(data.id);
	                console.log(data.title);
	                console.log(data.domain);
	                console.log(data.image);
	                console.log(data.tags);
	                console.log(data.link);
	                $('.card-lists #img-'+temp+' .img-container img').replaceWith('<img src="'+data.image+'">')
	                $('.card-lists #img-'+temp+' .link-title').replaceWith('<div class="link-title">'+data.title+'</div>')
	            },
	        })
		 }
	})

	$("#searchForm #searchSubmit").click(function(e){
		e.preventDefault();
		var query = $('#searchForm .input-search').val();
		var formData = {
			'q': query,
		}
		$.ajax({
			type: 'GET',
			url: '/'+slug+'/search',
			data: formData,
			success: function(data) {
				console.log(data);
			}
		})
	})

})







