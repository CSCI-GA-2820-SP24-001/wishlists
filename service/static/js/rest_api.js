$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#wishlist_id").val(res.id);
        $("#wishlist_title").val(res.title);
        $("#wishlist_user_id").val(res.user_id);
        $("#wishlist_count").val(res.count);
        $("#wishlist_description").val(res.description);
        $("#wishlist_items").val(res.items);
        $("#wishlist_date").val(res.date);
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#wishlist_title").val("");
        $("#wishlist_description").val("");
        $("#wishlist_date").val("");
        $("#wishlist_user_id").val("");
        $("#wishlist_count").val("");
        $("#wishlist_items").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a Wishlist
    // ****************************************

    $("#create-btn").click(function () {

        let title = $("#wishlist_title").val();
        let description = $("#wishlist_description").val();
        let count = $("#wishlist_count").val();
        let user_id = $("#wishlist_user_id").val();
        let items = $("#wishlist_items").val();
        let date = $("#wishlist_date").val();

        let data = {
            "title": title,
            "description": description,
            "items": items,
            "count": count,
            "user_id": user_id,
            "date": date
        };

        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "POST",
            url: "/wishlists",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // TODO: Update a Wishlist
    // ****************************************

    $("#update-btn").click(function () {

        let wishlist_id = $("#wishlist_id").val();
        let title = $("#wishlist_title").val();
        let description = $("#wishlist_description").val();
        let count = $("#wishlist_count").val();
        let user_id = $("#wishlist_user_id").val();
        let items = $("#wishlist_items").val();
        let date = $("#wishlist_date").val();

        let data = {
            "title": title,
            "description": description,
            "items": items,
           "count": count,
            "user_id": user_id,
            "date": date
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
                type: "PUT",
                url: `/wishlists/${wishlist_id}`,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve a Wishlist
    // ****************************************

    $("#retrieve-btn").click(function () {

        let wishlist_id = $("#wishlist_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/wishlists/${wishlist_id}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

     // ****************************************
     // Delete a Wishlist
     // ****************************************

     $("#delete-btn").click(function () {

         let wishlist_id = $("#wishlist_id").val();

         $("#flash_message").empty();

         let ajax = $.ajax({
             type: "DELETE",
             url: `/wishlists/${wishlist_id}`,
             contentType: "application/json",
             data: '',
         })

         ajax.done(function(res){
             clear_form_data()
             flash_message("Wishlist has been Deleted!")
         });

         ajax.fail(function(res){
             flash_message("Server error!")
         });
     });

     // ****************************************
     // Clear the form
     // ****************************************

     $("#clear-btn").click(function () {
         $("#wishlist_id").val("");
         $("#flash_message").empty();
         clear_form_data()
     });

     // ****************************************
     // Search for a wishlist (list and query)
     // ****************************************

    $("#search-btn").click(function () {

         let title = $("#wishlist_title").val();
         let description = $("#wishlist_description").val();
         let user_id = $("#wishlist_user_id").val();

         let queryString = ""

         if (title) {
             queryString += 'title=' + title
         }
         if (description) {
             if (queryString.length > 0) {
                 queryString += '&description=' + description
             } else {
                 queryString += 'description=' + description
             }
         }
         if (user_id) {
             if (queryString.length > 0) {
                 queryString += '&user_id=' + user_id
             } else {
                 queryString += 'user_id=' + user_id
             }
         }

         $("#flash_message").empty();

         let ajax = $.ajax({
             type: "GET",
             url: `/wishlists?${queryString}`,
             contentType: "application/json",
             data: ''
         })

         ajax.done(function(res){
             alert(res.toSource())
             $("#search_results").empty();
             let table = '<table class="table table-striped" cellpadding="10">'
             table += '<thead><tr>'
             table += '<th class="col-md-2">ID</th>'
             table += '<th class="col-md-2">Title</th>'
             table += '<th class="col-md-2">Description</th>'
             table += '<th class="col-md-2">User_ID</th>'
             table += '<th class="col-md-2">Items</th>'
             table += '<th class="col-md-2">Date</th>'
             table += '</tr></thead><tbody>'
             let firstWishlist = "";
             for(let i = 0; i < res.length; i++) {
                 let wishlist = res[i];
                 table +=  `<tr id="row_${i}"><td>${wishlist.id}</td><td>${wishlist.title}</td><td>${wishlist.description}</td><td>${wishlist.user_id}</td><td>${wishlist.items}</td><td>${wishlist.date}</td></tr>`;
                 if (i == 0) {
                     firstWishlist = wishlist;
                 }
             }
             table += '</tbody></table>';
             $("#search_results").append(table);

             // copy the first result to the form
             if (firstWishlist != "") {
                 update_form_data(firstWishlist)
             }

             flash_message("Success")
         });

         ajax.fail(function(res){
             flash_message(res.responseJSON.message)
         });

     });

     // ****************************************
     // Action for a wishlist (clear a wishlist)
     // ****************************************
     
    $("#clear-btn").click(function () {
         let wishlist_id = $("#wishlist_id").val();

         $("#flash_message").empty();

         let ajax = $.ajax({
             type: "POST", // or PUT or PATCH depending on your API design
             url: `/wishlists/${wishlist_id}/clear`, // or another endpoint designed for clearing a wishlist
             contentType: "application/json",
             data: ''
         })

         ajax.done(function (res) {
             clear_form_data()
             flash_message("Wishlist cleared successfully.")
         });
    
         ajax.fail(function(res){
             flash_message("Server error!") // Adjust error message if needed
         });

     });
})
