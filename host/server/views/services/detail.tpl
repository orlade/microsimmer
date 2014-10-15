% rebase('base.tpl', title='{{package}}/{{service}} Detail')

<h2>{{service}}</h2>

% include('forms/invoke.tpl', package=package, service=service, params=params)