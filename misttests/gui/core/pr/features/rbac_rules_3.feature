@rbac-rules-3
Feature: RBAC

  @create-users-org-team
  Scenario: Owner creates a new organization and adds a Softlayer cloud
    Given rbac members, organization and team are initialized
    Given I am logged in to mist.core
    Then I expect for "addBtn" to be clickable within max 20 seconds
    Given cloud "Docker" has been added via API request
    And script "touch_kati" is added via API request

  @add-member1
  Scenario: Add member1 and ALLOW-script-ALL
    When I visit the Teams page
    And I click the "Test team" "team"
    Then I expect the "team" edit form to be visible within max 5 seconds
    When I click the button "Invite Members" in "team" edit form
    Then I expect the "members" add form to be visible within max 5 seconds
    When I set the value "MEMBER1_EMAIL" to field "Emails" in "members" add form
    Then I expect for the button "Add" in "members" add form to be clickable within 2 seconds
    When I click the button "Add" in "members" add form
    Then I expect the "team" edit form to be visible within max 5 seconds
    And user with email "MEMBER1_EMAIL" should be pending
    When I focus on the button "Add a new rule" in "policy" edit form
    And I click the button "Add a new rule" in "policy" edit form
    And I wait for 1 seconds
    Then I add the rule always "ALLOW" "script" "all"
    And I click the button "Save Policy" in "policy" edit form
    And I wait for 2 seconds
    Then I logout

  @view-and-delete-script-success
  Scenario: Verify that member1 cannot view the machine created above
    Then I should receive an email at the address "MEMBER1_EMAIL" with subject "[mist.io] Confirm your invitation" within 30 seconds
    And I follow the link inside the email
    Then I enter my rbac_member1 credentials for login
    And I click the sign in button in the landing page popup
    Given that I am redirected within 10 seconds
    And I wait for the links in homepage to appear
    When I ensure that I am in the "ORG_NAME" organization context
    And I visit the Teams page
    Then "Test Team" team should be present within 5 seconds
    When I visit the Scripts page
    Then "touch_kati" script should be present within 5 seconds
    When I select list item "touch_kati" script
    And I click the action "Delete" from the script list actions
    And I expect the dialog "Delete Script" is open within 4 seconds
    And I wait for 2 seconds
    And I click the "Delete" button in the dialog "Delete Script"
    And I expect the dialog "Delete Script" is closed within 4 seconds
    Then "touch_kati" script should be absent within 5 seconds
    And I logout

  @allow-all-read
  Scenario: ALLOW-ALL-READ
    Given I am logged in to mist.core as rbac_owner
    And I visit the Teams page
    When I click the "Test team" "team"
    Then I expect the "team" edit form to be visible within max 5 seconds
    When I focus on the button "Add a new rule" in "policy" edit form
    And I click the button "Add a new rule" in "policy" edit form
    And I wait for 1 seconds
    Then I add the rule always "ALLOW" "all" "read"
    And I click the button "Save Policy" in "policy" edit form
    And I wait for 2 seconds
    Then I logout

  @member1-view-cloud-and-machine-success
  Scenario: Verify that member1 can view cloud and machine
    Given I am logged in to mist.core as rbac_member1
    And I ensure that I am in the "ORG_NAME" organization context
    When I visit the Machines page
    Then "testerrr" machine should be present within 5 seconds
    When I visit the Home page
    Then I should have 1 clouds added
