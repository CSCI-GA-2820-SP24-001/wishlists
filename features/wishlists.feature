Feature: The store service back-end
    As a Store Owner
    I need a RESTful catalog service
    So that I can keep track of all my wishlists

Background:
    Given the following wishlists
        | title      | description                | date       | user_id | count |
        | summer     | items for summer           | 2019-11-18 | 5431    | 5     |
        | trip       | items for hawaii           | 2020-08-13 | 8231    | 6     |
        | birthday   | items for spring birthday  | 2021-04-01 | 6783    | 7     |
        | holidays   | items for christmas        | 2018-06-04 | 2035    | 3     |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Wishlists RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Create a Wishlist
    When I visit the "Home Page"
    And I set the "Title" to "Christmas"
    And I set the "Description" to "Shopping list"
    And I set the "User ID" to "1234"
    And I set the "Count" to "8"
    And I set the "Date" to "12-12-2020"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clearform" button
    Then the "Id" field should be empty
    And the "Title" field should be empty
    And the "Description" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Christmas" in the "Title" field
    And I should see "Shopping list" in the "Description" field
    And I should see "1234" in the "User ID" field
    And I should see "8" in the "Count" field
    And I should see "2020-12-12" in the "Date" field
    
Scenario: Update a Wishlist
    When I visit the "Home Page"
    And I set the "Title" to "summer"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "summer" in the "Title" field
    And I should see "items for summer" in the "Description" field
    When I change "Title" to "trip"
    And I change "Description" to "updated trip"
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clearform" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "trip" in the "Title" field
    When I press the "Clearform" button
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "trip" in the results
    And I should not see "summer" in the results

Scenario: Delete a Wishlist
    When I visit the "Home Page"
    And I set the "Title" to "Christmas"
    And I set the "Description" to "Shopping list"
    And I set the "User ID" to "1234"
    And I set the "Count" to "8"
    And I set the "Date" to "12-12-2020"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clearform" button
    And I paste the "Id" field
    And I press the "Delete" button
    Then I should see the message "Wishlist has been Deleted!"
    When I copy the "Id" field
    And I press the "Clearform" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "404 Not Found"

Scenario: List all Wishlists
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "summer" in the results
    And I should see "trip" in the results
    And I should not see "fall" in the results

Scenario: Search (query) for items for summer
    When I visit the "Home Page"
    And I set the "Description" to "items for summer"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "summer" in the results
    And I should not see "Christmas" in the results

Scenario: Read / get a Wishlist
    When I visit the "Home Page"
    And I set the "Title" to "summer"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "summer" in the "Title" field
    And I should see "items for summer" in the "Description" field
    When I copy the "Id" field
    And I press the "Clearform" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "summer" in the "Title" field
    And I should see "items for summer" in the "Description" field

Scenario: Duplicate a Wishlist
    When I visit the "Home Page"
    And I set the "Title" to "Christmas"
    And I set the "Description" to "Shopping list"
    And I set the "User ID" to "1234"
    And I set the "Count" to "8"
    And I set the "Date" to "12-12-2020"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Duplicate" button
    Then I should see the message "Success"
    When I press the "Search" button
    Then I should see the message "Success"
    And I should see "Christmas COPY" in the results



