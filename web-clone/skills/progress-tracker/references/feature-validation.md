# Feature Validation Guide

This guide provides comprehensive instructions for validating features in autonomous coding projects.

## Validation Process Overview

Feature validation ensures that implemented features meet all requirements through end-to-end testing with browser automation.

## Pre-Validation Checks

Before validating a feature, ensure:

1. **Implementation is complete** - All code written
2. **Server is running** - Development environment active
3. **Database ready** - Test data available if needed
4. **Browser accessible** - Can navigate to app URL

## Validation Steps

### Step 1: Read Feature Requirements

Review the feature in `.spec/feature_list.json`:

```json
{
  "id": 1,
  "category": "functional",
  "description": "User can login with email and password",
  "steps": [
    "Navigate to /login",
    "Enter email and password",
    "Click submit button",
    "Verify redirect to dashboard"
  ],
  "passes": false
}
```

Understand:
- What the feature does
- Each test step
- Expected outcome

### Step 2: Prepare Test Environment

1. Start development server:
   ```bash
   ./.spec/init.sh
   ```

2. Verify server is running:
   ```bash
   curl http://localhost:3000
   ```

3. Prepare test data if needed:
   - Create test user
   - Set up test scenarios
   - Clear previous test data

### Step 3: Execute Test Steps

For each step in the feature's steps array:

1. **Navigate** to starting page
2. **Perform** the action described
3. **Capture** screenshot
4. **Verify** expected result
5. **Check** for console errors

### Step 4: Comprehensive Testing

Beyond the basic steps, also test:

#### Edge Cases
- Empty inputs
- Invalid data
- Boundary conditions
- Error states
- Network failures

#### User Flows
- Happy path (normal usage)
- Alternative paths
- Back navigation
- Refresh/reload
- Multiple attempts

#### Visual Verification
- Layout correctness
- Typography
- Colors
- Spacing
- Alignment
- Responsiveness

### Step 5: Document Results

Capture documentation:

1. **Screenshots** - Each step with descriptive names
2. **Console output** - Zero errors expected
3. **Notes** - Any issues or deviations

### Step 6: Update Status

Only after ALL verification passes:

1. Update `.spec/feature_list.json`:
   ```json
   "passes": true
   ```

2. Update `.spec/claude-progress.txt` with notes

3. Commit changes:
   ```bash
   git add .spec/feature_list.json
   git commit -m "Implement feature #N - verified end-to-end"
   ```

## Validation Checklist

Use this checklist before marking feature as passing:

### Functionality
- [ ] All test steps completed successfully
- [ ] Expected behavior verified
- [ ] Edge cases tested
- [ ] Error handling works
- [ ] No regressions

### Visual
- [ ] Layout matches requirements
- [ ] Typography correct
- [ ] Colors match spec
- [ ] Spacing consistent
- [ ] Alignment proper
- [ ] Responsive design works

### Technical
- [ ] Zero console errors
- [ ] No network failures
- [ ] Performance acceptable
- [ ] Accessibility OK
- [ ] Code quality good

### Documentation
- [ ] Screenshots captured
- [ ] Test results documented
- [ ] Issues noted (if any)
- [ ] Progress notes updated

## Common Validation Issues

### Issue: Element Not Found

**Symptoms:** Can't find button/input to interact with

**Solutions:**
- Wait for element to appear
- Use more specific selector
- Check if element exists in current state
- Verify page loaded completely

### Issue: Timeout Errors

**Symptoms:** Test hangs or times out

**Solutions:**
- Increase timeout
- Check server responsiveness
- Verify network connectivity
- Add explicit waits

### Issue: Console Errors

**Symptoms:** Errors in browser console

**Solutions:**
- Note error messages
- Identify root cause
- Fix the bug
- Re-test completely

### Issue: Visual Problems

**Symptoms:** Layout issues, broken UI

**Solutions:**
- Capture screenshot showing issue
- Document expected vs actual
- Fix CSS/layout bug
- Re-verify with new screenshot

### Issue: Inconsistent Results

**Symptoms:** Test passes sometimes, fails others

**Solutions:**
- Add explicit waits
- Use stable selectors
- Avoid time-based assertions
- Fix race conditions

## Regression Testing

When implementing new features, always verify previous features:

1. **Select 1-2 core features** that are "passes": true
2. **Run their complete test flows**
3. **Verify they still work**
4. **If broken:**
   - Mark as "passes": false
   - Add to regression list
   - Fix before proceeding
   - Re-verify

## Validation Anti-Patterns

### Don't Skip Steps

❌ **Bad:** Test only the final outcome
✅ **Good:** Test each step individually

### Don't Use Shortcuts

❌ **Bad:** Use JavaScript evaluation to bypass UI
✅ **Good:** Interact through UI like a human

### Don't Ignore Console

❌ **Bad:** Overlook console errors
✅ **Good:** Fix all errors before marking passing

### Don't Skip Visuals

❌ **Bad:** Only test functionality
✅ **Good:** Verify visual appearance too

### Don't Assume

❌ **Bad:** Assume it works without testing
✅ **Good:** Verify with screenshots and evidence

## Validation Best Practices

### 1. Test Like a User

Interact with the UI the way a human would:
- Click visible elements
- Type in visible fields
- Follow visual flows
- Use mouse and keyboard

### 2. Be Thorough

Don't cut corners:
- Test all steps
- Test edge cases
- Test error states
- Test multiple times

### 3. Document Everything

Keep records:
- Screenshots for each step
- Console output
- Test notes
- Issues found

### 4. Fix Issues First

Before marking as passing:
- Fix all bugs
- Resolve all errors
- Address visual issues
- Re-test completely

### 5. Be Skeptical

Question results:
- Test multiple times
- Try different approaches
- Verify assumptions
- Look for edge cases

## Conclusion

Feature validation is the quality gate for autonomous coding. Thorough validation ensures production-ready features that work correctly and look professional.

Remember: Only mark a feature as "passes": true after complete verification with screenshots and zero console errors.
