% rebase('base.tpl', title='Home')

<h2>Register New Container</h2>
<form method="POST" action="/services/register">
    Docker ID: <input name="docker_id" />
    <input type="submit" />
</form>

% if services:
<h2>Registered Containers</h2>
% include('services/list.tpl', services=services)
%end