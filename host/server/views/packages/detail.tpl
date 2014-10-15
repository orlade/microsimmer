% rebase('base.tpl', title='{{package}} Detail')

<h2>{{package}}</h2>
<div></div><a href="/packages/{{package}}/unregister">unregister</a></div>

<h3>Services</h3>

% include('services/list.tpl', package=package, services=services)