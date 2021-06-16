$('#register').on('click', function(evt) {
    window.location.href = '/user/register'
})
$(document).ready(function() {
    $('.alert').fadeIn().delay(500).fadeOut();
});
$('#back').on('click', function(evt) {
    window.history.back();
})
$('#back_link').on('click', function(evt) {
    window.history.back();
})

$('div').on('click', function(evt) {  
    if (evt.target.id === 'slider') {
        const parent = evt.target.parentNode;
        const ind = parent.id.indexOf('f');
        const id = parent.id.substr(0,ind);
        const val = evt.target.value;
        $(`#${id}rate`).text(`${val}/5`)
    };
})

// Favorites Functions
$('#fav').on('click', function(evt) {
    evt.preventDefault();
    const ind = evt.target.parentNode.id.indexOf('f');
    const id = evt.target.parentNode.id.substr(0,ind);
    const classes = evt.target.parentNode.classList;
    if (classes.contains('fav-off')) {
        evt.target.parentNode.classList.remove('fav-off')
        evt.target.parentNode.classList.add('fav-on')
    } else {
        evt.target.parentNode.classList.remove('fav-on')
        evt.target.parentNode.classList.add('fav-off')
    }
    addFav(id);
    setTimeout(function() { get_user_favorites_page(); }, 100);
})

function get_user_favorites_page() {
    window.location.href = '/user/favorites'
}

async function addFav(id) {
    await axios.post('/user/favorites', {
        drinkId: id
    });
};

// User Rating
$('#rate_btn').on('click', function(evt) {
    evt.preventDefault();
    const slider = evt.target.nextElementSibling.nextElementSibling
    const rating = slider.value
    const ind = evt.target.parentNode.id.indexOf('f');
    const id = evt.target.parentNode.id.substr(0,ind);
    addRate(rating, id);

})

async function addRate(rating, id) {
    await axios.post(`/drinks/${id}`, {
        rating: rating
    });
}

// Removing Favorited
$('.fav-remove').on('click', function(evt) {
    const ind = evt.target.id.indexOf('r');
    const id = evt.target.id.substr(0,ind);
    removeFav(id);
    setTimeout(function() { get_user_favorites_page(); }, 100);
})

async function removeFav(id) {
    await axios.post('/user/favorites', {
        drinkId: id
    });
};

// User Recommending/Removal
$('.btn-success').on('click', function(evt) {
    const ind = evt.target.id.indexOf('r');
    const id = evt.target.id.substr(0,ind);
    window.location.href = `/user/recommend/form${id}`
})

$('.rec-remove').on('click', function(evt) {
    const ind = evt.target.id.indexOf('r');
    const id = evt.target.id.substr(0,ind);
    removeRecommend(id);
    setTimeout(function() { get_recommends_page(); }, 100);
})

async function removeRecommend(id) {
    await axios.post('/user/recommendations', {
        recId: id
    });
};

function get_recommends_page() {
    window.location.href = '/user/recommendations'
}