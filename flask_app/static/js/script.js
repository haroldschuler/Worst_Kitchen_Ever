function redirect_to_recipe(recipe_id) {
    location.href = '/recipes/recipe/' + recipe_id;
}

function recipe_box_mouseover(element) {
    element.style.border = "2px solid black";
    element.style.padding = "23px";
    element.style.boxShadow = "2px 2px 2px";
    element.style.cursor = "pointer";
}

function recipe_box_mouseout(element) {
    element.style.border = "0px";
    element.style.padding = "25px";
    element.style.boxShadow = "0px 0px 0px";
}

function selection_box_mouseover(element) {
    element.style.border = "1px solid black";
    element.style.padding = "4px";
    element.style.boxShadow = "1px 1px 1px";
    element.style.cursor = "pointer";
}

function selection_box_mouseout(element) {
    element.style.border = "0px";
    element.style.padding = "5px";
    element.style.boxShadow = "0px 0px 0px";
}

function select_ingredient(element) {
    console.log(element.innerText);
    var ingredient_list = document.getElementById('selected_ingredients');
    // ingredient_list.innerHTML += `<p>${element.innerText}</p>`
    ingredient_list.innerHTML += `<div><input type="checkbox" name="${element.innerText}" class="ingredient_checkbox" id="chosen_ingredient_${element.innerText}" onclick="if_unchecked(this)" checked><label for="chosen_ingredient_${element.innerText}">${element.innerText}</label><br></br></div>`
    // onclick="if_unchecked(this)"
}

function if_unchecked(element) {
    if(element.checked == false) {
        var parent = element.parentNode
        console.log(parent)
        parent.remove();
    }
}

function add_item_to_shopping_list(element) {
    var item = element.innerText;
    console.log(item)
    var form = new FormData();
    form.append('item',item)
    fetch("http://localhost:5000/recipes/add_to_shopping_list", {method : 'POST', body : form})
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(err => console.log(err))
    location.reload();
}

function remove_from_list(element) {
    var item_id = element.value;
    console.log(item_id)
    var form = new FormData();
    form.append('item_id',item_id)
    fetch("http://localhost:5000/recipes/remove_from_shopping_list", {method : 'POST', body : form})
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(err => console.log(err))
    location.reload();
}

// function clear_shopping_list() {
//     // var form = new FormData();
//     // form.append('item_id',item_id)
//     fetch("http://localhost:5000/recipes/clear_list", {method : 'POST'})
//     .then(response => response.json())
//     .then(data => console.log(data))
//     .catch(err => console.log(err))
//     location.reload();
// }

function search_bar_results(element) {
    var search_value = document.getElementById('ingredient_input_bar')
    // var myForm = document.getElementById('ingredient_search_form');
    search_value.oninput = function(event) {
        event.preventDefault();
        var form = new FormData();
        form.append('value',element.value);
        fetch("http://localhost:5000/search_ingredients", {method :'POST', body : form})
        .then(response => response.json())
        .then(data => {
            // console.log(data)
            console.log(data.counter)
            var counter = data.counter;
            var dropdown = document.getElementById('dropdown');
            var dropdown_left = document.getElementById('dropdown_left_column');
            var dropdown_right = document.getElementById('dropdown_right_column');
            if(counter == 1000 || counter == 0) {
                dropdown.style.display = "none";
                dropdown.children.style.display = "none";
                document.getElementsByClassName('selection_block').display = "none"
            }
            for(let i = 1; i <= counter; i++) {
                dropdown.style.display = "flex"
                dropdown.style.backgroundColor = "rgb(125, 111, 134)"
                if(i == 1) {
                    // console.log(data.item1.ingredient_name)
                    dropdown_left.innerHTML = `<div class="selection_block" onmouseover="selection_box_mouseover(this)" onmouseout="selection_box_mouseout(this)" onclick="select_ingredient(this)"><p>${data.item1.ingredient_name}</p></div>`
                }
                if(i == 2) {
                    // console.log(data.item2.ingredient_name)
                    dropdown_right.innerHTML = `<div class="selection_block" onmouseover="selection_box_mouseover(this)" onmouseout="selection_box_mouseout(this)" onclick="select_ingredient(this)"><p>${data.item2.ingredient_name}</p></div>`
                }
                if(i == 3) {
                    // console.log(data.item3.ingredient_name)
                    dropdown_left.innerHTML += `<div class="selection_block" onmouseover="selection_box_mouseover(this)" onmouseout="selection_box_mouseout(this)" onclick="select_ingredient(this)"><p>${data.item3.ingredient_name}</p></div>`
                }
                if(i == 4) {
                    // console.log(data.item4.ingredient_name)
                    dropdown_right.innerHTML += `<div class="selection_block" onmouseover="selection_box_mouseover(this)" onmouseout="selection_box_mouseout(this)" onclick="select_ingredient(this)"><p>${data.item4.ingredient_name}</p></div>`
                }
                if(i == 5) {
                    // console.log(data.item5.ingredient_name)
                    dropdown_left.innerHTML += `<div class="selection_block" onmouseover="selection_box_mouseover(this)" onmouseout="selection_box_mouseout(this)" onclick="select_ingredient(this)"><p>${data.item5.ingredient_name}</p></div>`
                }
                if(i == 6) {
                    // console.log(data.item6.ingredient_name)
                    dropdown_right.innerHTML += `<div class="selection_block" onmouseover="selection_box_mouseover(this)" onmouseout="selection_box_mouseout(this)" onclick="select_ingredient(this)"><p>${data.item6.ingredient_name}</p></div>`
                }
            }
            // console.log(data.item2.ingredient_name)
            // console.log(data.item3.ingredient_name)
            // // console.log(data.item4.ingredient_name)

            // console.log(data.item6.ingredient_name)
            // console.log(data.item7.ingredient_name)
            // console.log(data.item8.ingredient_name)
            // console.log(data.item9.ingredient_name)
            // console.log(data.item10.ingredient_name)
        })
        .catch(err => console.log(err) )
    }
}

// *****************clearing session shopping list***************************
// may not be needed because it's ok if the page refreshes
// var shopping_list_clear_form = document.querySelector('#clear_shopping_list_form');

// shopping_list_clear_form.addEventListener("submit", function(event){
//     event.preventDefault()
//     var form = new FormData(shopping_list_clear_form)
//     fetch("http://localhost:5000/clear_shopping_list", {method :'POST', body : form})
//     .then(resp => resp.json())
//     .then(data => console.log(data))
// })
// function clear_shopping_list() {
//     fetch("http://localhost:5000/clear_shopping_list", {method :'POST'})
//     .then(resp => resp.json())
//     .then(data => console.log(data))
// }
// *****************************************************************************

// format api call: https://api.spoonacular.com/food/products/search?query=yogurt&apiKey=API-KEY
var api_key = '1259ebb6297343a79a643091713a9e79';
var number = 2; 
var ranking = 1; //1 will maximized used ingredient, 2 will minimize missing ingredients

var submit_ingredients_form = document.querySelector("#submit_ingredients_form");

// submit_ingredients_form.addEventListener("submit",function(event){
//     event.preventDefault()
//     console.log(submit_ingredients_form.children[0]);
// })

function call_recipe_api() {
    fetch(`https://api.spoonacular.com/recipes/findByIngredients?apiKey=${api_key}&ingredients=apples,+flour,+sugar&number=${number}`)
    // fetch('www.themealdb.com/api/json/v1/1/filter.php?i=chicken_breast')
    .then(resp => resp.json())
    .then(data => {
        console.log(data);
        console.log(data[0]);
        console.log(data[0]['title']);
        
    })
    .catch(err => console.log(err))
}

var test_recipe_id = 640352;

function call_recipe_by_id_api() {
    fetch(`https://api.spoonacular.com/recipes/${test_recipe_id}/information?apiKey=${api_key}`)
    .then(resp => resp.json())
    .then(data => {
        console.log(data);
    })
    .catch(err => console.log(err))
}