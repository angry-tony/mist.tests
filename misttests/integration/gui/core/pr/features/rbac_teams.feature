@rbac-teams
Feature: Rbac

  @create-org
  Scenario: Owner creates a new organization
    Given rbac member1 has been registered
    Given I am logged in to mist.core
    When I click the Gravatar
    And I wait for 1 seconds
    And I click the button "Add Organization" in the user menu
    Then I expect the dialog "Add Organization" is open within 4 seconds
    And I wait for 1 seconds
    When I set the value "ORG_NAME" to field "Name" in "Add Organization" dialog
    And I click the "Add" button in the dialog "Add Organization"
    And I wait for 2 seconds
    And I click the "Switch" button in the dialog "Add Organization"
    Then I expect the dialog "Add Organization" is closed within 4 seconds
    And I wait for 1 seconds

  @create-dup-org
  Scenario: Creating an org with the name used above, should bring a 409 error
    When I click the Gravatar
    And I wait for 1 seconds
    And I click the button "Add Organization" in the user menu
    Then I expect the dialog "Add Organization" is open within 4 seconds
    And I wait for 1 seconds
    When I set the value "ORG_NAME" to field "Name" in "Add Organization" dialog
    And I click the "Add" button in the dialog "Add Organization"
    And I wait for 2 seconds
    Then there should be a "409" error message in "Add Organization" dialog
    And I click the "Cancel" button in the dialog "Add Organization"
    And I wait for 1 seconds

  @add-team
  Scenario: Owner creates a team
    When I visit the Teams page
    When I click the button "+"
    Then I expect the dialog "Add Team" is open within 4 seconds
    When I set the value "Test Team" to field "Name" in "Add Team" dialog
    And I click the "Add" button in the dialog "Add Team"
    When I visit the Teams page
    Then "Test Team" team should be present within 5 seconds

  @add-member1
  Scenario: Add member1
    When I visit the Home page
    When I refresh the page
    And I wait for the links in homepage to appear
    And I visit the Teams page
    When I click the "Test team" "team"
    And I expect the "team" edit form to be visible within max 8 seconds
    Then I click the button "Invite" in "team" edit form
    And I expect the "members" add form to be visible within max 5 seconds
    When I set the value "MEMBER1_EMAIL" to field "Emails" in "members" add form
    Then I expect for the button "Add" in "members" add form to be clickable within 2 seconds
    And I click the button "Add" in "members" add form
    And I expect the "team" edit form to be visible within max 5 seconds
    Then user with email "MEMBER1_EMAIL" should be pending
    Then I logout
    Then I should receive an email at the address "MEMBER1_EMAIL" with subject "Confirm your invitation" within 60 seconds
    And I follow the link inside the email
    And I wait for 2 seconds
    Then I enter my rbac_member1 credentials for login
    And I click the sign in button in the landing page popup
    Given that I am redirected within 5 seconds
    And I wait for the links in homepage to appear
    Then I ensure that I am in the "ORG_NAME" organization context
    When I visit the Teams page
    Then "Test Team" team should be present within 5 seconds
    Then I logout

   @add-member2
   Scenario: Add member2
    Given I am logged in to mist.core as rbac_owner
    And I visit the Teams page
    When I click the "Test team" "team"
    And I expect the "team" edit form to be visible within max 5 seconds
    Then I click the button "Invite" in "team" edit form
    And I expect the "members" add form to be visible within max 5 seconds
    When I set the value "MEMBER2_EMAIL" to field "Emails" in "members" add form
    Then I expect for the button "Add" in "members" add form to be clickable within 2 seconds
    And I click the button "Add" in "members" add form
    And I expect the "team" edit form to be visible within max 5 seconds
    Then user with email "MEMBER2_EMAIL" should be pending
    And user with email "MEMBER1_EMAIL" should be confirmed
    Then I logout
    Then I should receive an email at the address "MEMBER2_EMAIL" with subject "Confirm your invitation" within 60 seconds
    And I follow the link inside the email
    And I wait for 2 seconds
    Then I enter my rbac_member2 credentials for signup_password_set
    And I click the go button in the landing page popup
    And I wait for the links in homepage to appear
    Then I ensure that I am in the "ORG_NAME" organization context
    When I visit the Teams page
    And "Test Team" team should be present within 5 seconds
    Then I logout

  @delete-members
  Scenario: Owner deletes team members
    Given I am logged in to mist.core as rbac_owner
    And I visit the Teams page
    And I wait for 3 seconds
    When I click the "Test Team" "team"
    And I expect the "team" edit form to be visible within max 5 seconds
    Then user with email "MEMBER2_EMAIL" should be confirmed
    When I delete user "MEMBER2_EMAIL" from team
    And I expect the dialog "Delete Member from Team" is open within 4 seconds
    And I click the "Delete" button in the dialog "Delete Member from Team"
    And I expect the dialog "Delete Member from Team" is closed within 4 seconds
    When I delete user "MEMBER1_EMAIL" from team
    And I expect the dialog "Delete Member from Team" is open within 4 seconds
    And I click the "Delete" button in the dialog "Delete Member from Team"
    And I expect the dialog "Delete Member from Team" is closed within 4 seconds

  @rename-team
  Scenario: Owner renames a team
    Then I click the button "Edit" in "team" edit form
    And I expect the dialog "Edit Team" is open within 4 seconds
    Then I expect the field "Name" in the dialog with title "Edit Team" to be visible within max 2 seconds
    When I set the value "Rbac Team" to field "Name" in "Edit Team" dialog
    And I wait for 1 seconds
    And I click the "Submit" button in the dialog "Edit Team"
    And I expect the dialog "Edit Team" is closed within 4 seconds
    Then I visit the Home page
    Then I visit the Teams page
    And "Test Team" team should be absent within 5 seconds
    And "Rbac Team" team should be present within 5 seconds
    Then I logout

 @verify-delete-member
  Scenario: Member2 has been removed from org
    Given I am logged in to mist.core as rbac_member2
    Then I should see the form to set name for new organization
    Then I logout

  @delete-team
  Scenario: Owner deletes a team
    Given I am logged in to mist.core as rbac_owner
    When I visit the Teams page
    When I click the "Rbac Team" "team"
    And I expect the "team" edit form to be visible within max 5 seconds
    Then I click the button "Delete" in the "team" page actions menu
    And I expect the dialog "Delete Team" is open within 4 seconds
    And I click the "Delete" button in the dialog "Delete Team"
    Then I expect the dialog "Delete Team" is closed within 4 seconds
    Then I visit the Home page
    And I wait for 2 seconds
    And I visit the Teams page
    And "Rbac Team" team should be absent within 10 seconds

#  @tag-team
#  Scenario: Owner tags a team
#    Given I am logged in to mist.core as rbac_owner
#    When I wait for the dashboard to load
#    And I visit the Teams page
#    When I click the button "tag" from the menu of the "Rbac Team" team
#    And I expect for the tag popup to open within 4 seconds
#    When I remove all the previous tags
#    Then I add a tag with key "team" and value "ops"
#    And I click the button "Save Tags" in the tag menu
#    Then I expect for the tag popup to close within 4 seconds
#    And I wait for 2 seconds
#    Then I ensure that the "team" has the tags "team:ops"
