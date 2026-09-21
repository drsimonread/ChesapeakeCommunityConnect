JQuery/HTML Info/Links

Collected by Quinnten Hatfield and Anthony Walsh

[**Pagination example:	1**](#pagination-example:)

[**Pagination Draft:	2**](#pagination-draft:)

[**JQuery Youtube Tutorial (Last few include AJAX)	2**](#jquery-youtube-tutorial-\(last-few-include-ajax\))

[**How to check if you have hit the bottom of the page	2**](#how-to-check-if-you-have-hit-the-bottom-of-the-page)

[**Using Django Paginator Class	3**](#using-django-paginator-class)

[**Link to Regular Django Python pagination video	4**](#link-to-regular-django-python-pagination-video)

# 

# 

# **Pagination example:** {#pagination-example:}

Uses Jquery plugin Pagination.js

$(function() {   
var container \= $('\#demo');   
container.pagination({   
dataSource:'https://api.flickr.com/services/feeds/photos\_public.gne?tags=cat\&tagmode=any\&format=json\&jsoncallback=?',   
locator: 'items',  
totalNumber: 20,   
pageSize: 3,   
ajax: {   
beforeSend: function() {   
container.prev().html('Loading data from flickr.com ...');   
}   
},   
callback: function(response, pagination) {   
var dataHtml \= '\<ul\>';   
var pageStart \= (pagination.pageNumber \- 1) \* pagination.pageSize;  
var pageEnd \= pageStart \+ pagination.pageSize;  
var pageItems \= response.slice(pageStart, pageEnd);  
$.each(pageItems, function(index, item) {   
dataHtml \+= '\<li\>' \+ item.title \+ '\</li\>';   
}); 

dataHtml \+= '\</ul\>'; 

container.prev().html(dataHtml);   
}   
})   
})

Pagination.js link showing how to use it: [https://pagination.js.org/](https://pagination.js.org/)

# **Pagination Draft:** {#pagination-draft:}

$(‘\#demo’).pagination({  
	dataSource: (Url for forums),  
	locator: ‘items’,  
	totalNumberLocator: function(response) {  
		return response.total;  
	},  
	pageSize: 10,  
	ajax: {  
		beforeSend: function() {  
			dataContainer.html(‘Loading Forums…’);  
		}  
	},  
	callback: function(data, pagination) {  
		var html \= template(data);  
		dataContainer.html(html);  
	}  
})

# **JQuery Youtube Tutorial (Last few include AJAX)** {#jquery-youtube-tutorial-(last-few-include-ajax)}

[https://www.youtube.com/playlist?list=PLoYCgNOIyGABdI2V8I\_SWo22tFpgh2s6\_](https://www.youtube.com/playlist?list=PLoYCgNOIyGABdI2V8I_SWo22tFpgh2s6_)

# **How to check if you have hit the bottom of the page** {#how-to-check-if-you-have-hit-the-bottom-of-the-page}

$(window).scroll(function() {   
if($(window).scrollTop() \== $(document).height() \- $(window).height()) {  
 // ajax call get data from server and append to the div   
}   
});

# **Using Django Paginator Class** {#using-django-paginator-class}

  from django.core.paginator import Paginator

  def my\_view(request):  
      objects \= MyModel.objects.all()  
      paginator \= Paginator(objects, 10)  *\# 10 items per page*

      page\_number \= request.GET.get('page')  
      page\_obj \= paginator.get\_page(page\_number)

      context \= {  
          'page\_obj': page\_obj,  
      }  
      return render(request, 'my\_template.html', context)

**How to use ajax to call data from the server**  
This is an example of loading a document using ajax  
[https://www.w3schools.com/js/js\_ajax\_http.asp](https://www.w3schools.com/js/js_ajax_http.asp)

function loadDoc() {  
	const xhttp \= new XMLHttpRequest();  
	xhttp.onload \= function() {  
		document.getElementById(“demo”).innerHTML \= this.responseText;  
	}  
	xhttp.open(“GET”, “forums url”, true);  
	xhttp.send();  
}  
getElementById(): gets all html elements with id of whatever is in the parentheses, in the example above that would be “demo”.

innerHTML: allows you to get or set the html content inside the selected element.

this.responseText: This is the response from the server, typically in plain text or HTML format.

onload: Defines a function that is executed when the request receives an answer.

open: Specifies the type of request, (method, url, async)  
method: The type of request, either “GET” or “POST”.  
url: The server file location  
async: True (asynchronous) or False (synchronous)

send: sends the request to the server (used for GET)  
send(string): sends request to the server (used for POST)

# **Link to Regular Django Python pagination video** {#link-to-regular-django-python-pagination-video}

[https://youtu.be/N-PB-HMFmdo](https://youtu.be/N-PB-HMFmdo)

Code so far:	

\<div id\="forum-posts" class \= "has-text-dark mx-6"\>  
            {% for post in posts %}  
                {% if posts|length \< 10 %}  
                 
                {% include 'mapViewer/postTemplate.html' %}  
                 
                {% else %}  
                    \<script\>  
                        $(window).scroll(function() {  
                            if($(window).scrollTop() \== $(document).height() \- $(window).height()) {  
                                function loadDoc() {  
                                    const xhttp \= new XMLHttpRequest();  
                                    xhttp.onload \= function() {  
                                        document.getElementById(“forum\-posts”).innerHTML \= this.responseText;  
                                    }  
                                    xhttp.open(“GET”, "forum/\<int:want\>/", true);  
                                    xhttp.send();  
                                }  
                            }  
                        });  
                    \</script\>  
                {% endif %}

            {% empty %}  
            \<p class \= "ml-6 has-text-black"\>No posts available.\</p\>

            {% endfor %}  
        \</div\>  
