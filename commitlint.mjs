// See: https://commitlint.js.org/#/reference-configuration for details
// on the configuration file
module.exports = {
  extends: ['@commitlint/config-conventional'],

  rules: {
    'type-enum':
      [2, 'always', [
        'revert', 'feat', 'fix', 'perf', 'docs', 'test', 'build', 'refactor', 'style', 'chore', 'temp', 'ci',
      ]],

    // Default rules we want to suppress. The available list of rules can be
    // found in https://commitlint.js.org/#/reference-rules
    'body-leading-blank': [0, "always"],
    'body-max-line-length': [0, "always"],
    'footer-max-line-length': [0, "always"],
    'footer-leading-blank': [0, "always"],
    'subject-case': [0, "always", []],
    'subject-full-stop': [0, "never", '.'],
  },

  ignores: [
    // Allow GitHub revert messages, like:
    //    Revert "introduce a bug"
    //    Revert "introduce a bug" (#1234)
    message => /^Revert ".*"( \(#\d+\))?/.test(message),

    // BTW: commitlint has a built-in list of ignores which are also applied.
    // Those include the typical "Merged" messages, so those are implicitly ignored:
    // https://github.com/conventional-changelog/commitlint/blob/master/%40commitlint/is-ignored/src/defaults.ts
  ],
};
