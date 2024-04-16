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



