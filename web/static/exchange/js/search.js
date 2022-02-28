document.getElementById("inputBox").value = '';
var createdObj = []
function removeObj() {
    createdObj.forEach(function(item, index) {
        item.remove();
    })
    createdObj = []
}

function getCoins(query){
	main_url = window.location.origin;
	var url = `${main_url}/search/${query}`
    const xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.timeout = 30000;
    xhr.ontimeout = function () { console.log('time out'); }
    xhr.responseType = 'json';

    xhr.onreadystatechange = function(e) {
        if (this.status === 200 && xhr.readyState == 4) {
            var loading = document.getElementById("loading");
            var res = document.getElementById("res");
            resp = this.response;
            if (resp != 'null') {
            	Object.keys(resp).forEach(function(item, index) {
                    loading.classList.remove('d-block')
                    loading.classList.add('d-none')
					createReasult(resp[index]);
				})
            }
            else {
                loading.classList.remove('d-block')
                loading.classList.add('d-none')
            	res.classList.remove('d-none')
				res.classList.add('d-block')
            }
        }
        else {
            console.log(this.status)
        }
    };
    try {
        xhr.send();
    } catch(err) {
        console.log('error')
    }
}

function createReasult(data) {

    var parent = document.getElementById("searchParent")
    var before = document.getElementById("searchBefore")

    var image = document.createElement("img")
    var a = document.createElement("a")
    var li = document.createElement("li")
    var row = document.createElement("div")
    var coin = document.createElement("div")
    var name = document.createElement("div")
    var col = document.createElement("div")

    row.classList.add('row')
    coin.classList.add('col-6')
    col.classList.add('col-6')

    image.src = data['image']
    image.setAttribute('style', 'height:18px; margin-right: 10px;')
    coin.setAttribute('style', 'display:block ruby')
    name.innerText = data['name'] + ` (${data["symbol"]})`
    a.href = `/account/trade/${data["symbol"]}-USDT`

    coin.appendChild(image)
    coin.appendChild(name)
    row.appendChild(coin)
    row.appendChild(col)
    li.appendChild(row)
    a.appendChild(li)

    createdObj.push(a)

    parent.insertBefore(a, before)
}

function delay(callback, ms) {
  var timer = 0;
  return function() {
    var context = this, args = arguments;
    clearTimeout(timer);
    timer = setTimeout(function () {
      callback.apply(context, args);
    }, ms || 0);
  };
}

var searchTerm = '';
jQuery(document).ready(function($){

	$('.live-search-box').keyup(delay(function (e) {
		var res = document.getElementById("res");
        var loading = document.getElementById("loading");
		removeObj()
		searchTerm = $(this).val().toLowerCase();
		console.log(searchTerm)
		if (searchTerm != '') {
			res.classList.remove('d-block')
			res.classList.add('d-none')
            loading.classList.remove('d-none')
            loading.classList.add('d-block')
			getCoins(searchTerm)
		}
		else {
			res.classList.remove('d-none')
			res.classList.add('d-block')
		}
	}, 500));

  $(function() {     
	$('.live-search-box').on('click',function(e) {
			$('.live-search-list').toggle();
            document.getElementById("inputBox").value = '';
			if (searchTerm == '') {
				res.classList.remove('d-none')
				res.classList.add('d-block')
			}
		});
	});
});