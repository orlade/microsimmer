% rebase('base.tpl', title='{{name}} Detail')

<h2>{{name}}</h2>
<div></div><a href="/packages/{{name}}/unregister">unregister</a></div>

% include('forms/invoke.tpl')