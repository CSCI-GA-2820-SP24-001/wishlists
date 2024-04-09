Feature: The store service back-end
    As a Store Owner
    I need a RESTful catalog service
    So that I can keep track of all my wishlists

Background:
    Given the following wishlists
        | title       | description            | 
        | summer      | items for the summer   |    
        | trip        | items for my trip      |
        | holiday     | items for christmas    |
        | birthday    | clothes for my bday    |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Wishlist Demo RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Create a Wishlist
    When I visit the "Home Page"
    And I set the "Title" to "summer"
    And I set the "Description" to "items for the summer"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Title" field should be empty
    And the "Description" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "summer" in the "Title" field
    And I should see "items for the summer" in the "Description" field
    
Scenario: List all wishlists
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "summer" in the results
    And I should see "trip" in the results
    And I should not see "holiday" in the results
    And I should not see "birthday" in the results

Scenario: Search for title
    When I visit the "Home Page"
    And I set the "Title" to "trip"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "trip" in the results
    And I should not see "summer" in the results
    And I should not see "holiday" in the results
    And I should not see "birthday" in the results

Scenario: Update a Wishlist
    When I visit the "Home Page"
    And I set the "Title" to "summer"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "summer" in the "Title" field
    And I should see "items for the summer" in the "Description" field
    When I change "Title" to "may"
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "may" in the "Title" field
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "may" in the results
    And I should not see "summer" in the results