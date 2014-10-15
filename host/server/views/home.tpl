% rebase('base.tpl', title='Page Title')

<h2>Register New Container</h2>
<form method="POST" action="/services/register">
    Docker ID: <input name="docker_id" />
    <input type="submit" />
</form>

% if packages:
<h2>Registered Containers</h2>
<ul>
    % for package in packages:
    <li>{{package}}</li>
    % end
</ul>
%end