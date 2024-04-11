Feature: The store service back-end
    As a Store Owner
    I need a RESTful catalog service
    So that I can keep track of all my wishlists

Background:
    Given the following wishlists
        | title      | description                | items | date       | user id |
        | summer     | items for summer           | 2     | 2019-11-18 | 5431    |
        | trip       | items for hawaii           | 5     | 2020-08-13 | 8231    |
        | birthday   | items for spring birthday  | 7     | 2021-04-01 | 6783    |
        | holidays   | items for christmas        | 1     | 2018-06-04 | 2035    |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Wishlist Demo RESTful Service" in the title
    And I should not see "404 Not Found"




