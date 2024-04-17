Feature: The store service back-end
    As a Store Owner
    I need a RESTful catalog service
    So that I can keep track of all my wishlists

Background:
    Given the following wishlists
        | title      | description                | user_id    | date          | count |
        | summer     | items for summer           | 5473       | 2019-11-18    | 5     |
        | trip       | items for hawaii           | 8976       | 2020-08-13    | 6     |
        | birthday   | items for spring birthday  | 2345       |  2021-04-01   | 7     |
        | holidays   | items for christmas        | 6823       | 2018-06-04    | 3     |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Wishlists RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Update a Wishlist
    When I visit the "Home Page"
    And I set the "Title" to "summer"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "summer" in the "Title" field
    And I should see "items for summer" in the "Description" field
    When I change "Title" to "trip"
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Title" in the "Trip" field
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Trip" in the results
    And I should not see "summer" in the results