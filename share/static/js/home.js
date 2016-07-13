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
						'<div class="card"><div class="img-container"><img src="https://www.gapminder.org/GapminderMedia/wp-uploads/images_loaders/ajax-loader.gif"></div>'+'<div class="details"><div class="link-title">'+title+'</div></div><div class="hosts">'+
						'<span><object data="http://'+domain+'/favicon.ico" class="favicon-object" type="image/png"><img src="http://facebook.com/favicon.ico"></object></span><span class="host-name">'+
						domain+'</span><span class="pull-right tag"> <i class="fa fa-tag mar-r-5" aria-hidden="true"></i> </span>'+
						'</div><div class="clearfix"></div></div></a></div>'
					console.log(task)
					$('.card-lists').prepend(task);
	            },
	            success: function (data) {
	                console.log(data.title);
	                console.log(data.image);
	                console.log(data.tags);
	                $('.card-lists #img-'+temp+' .img-container img').replaceWith('<img src="'+data.image+'">')
	                $('.card-lists #img-'+temp+' .link-title').replaceWith('<div class="link-title">'+data.title+'</div>')
	            },
	        })
		 }
	})

	var delay = (function(){
	  var timer = 0;
	  return function(callback, ms){
	    clearTimeout (timer);
	    timer = setTimeout(callback, ms);
	  };
	})();

	$('#searchForm .input-search').keyup(function () {
		delay(function(){
			var newContent = $(this.target).val()
			searchLink(newContent)
	    }, 1000 );
    })

    function searchLink(value){
		var query = $('#searchForm .input-search').val();
		var formData = {
			'q': query,
		}
		if (query){
			$.ajax({
				type: 'GET',
				url: '/'+slug+'/search',
				data: formData,
				success: function(data) {
					$('#search-lists').empty();
					$.each(data, function(index){
						console.log(data[index].fields);
						getSearchData(data[index].fields);
					})
				}
			})
		} else {
			console.log('no data')
			$('#search-lists').empty();
		}
	}

	function getSearchData(data) {
		var markup = '<a href="'+data.link+'" target="_blank">';
			markup += '<div class="title">' + data.title + '</div>';
			markup += '<div class="hosts mar-t-5">' + data.domain + '</div>';
			markup += '</a>';

		return $('#search-lists').prepend(markup);
	}

	$('#editBoard').on('click', function(){
		$.ajax({
			type: 'GET',
			url: '/'+slug+'/edit',
			success: function(data) {
				$('#search-lists').empty();
				$.each(data, function(index){
					console.log(data[index].fields);
					getSearchData(data[index].fields);
				})
			}
		})
	})

})







