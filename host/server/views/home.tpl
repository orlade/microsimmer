% rebase('base.tpl', title='Home')

<h2>Register New Container</h2>
% include('forms/register.tpl')

% if services:
<h2>Registered Containers</h2>
% include('services/list.tpl', services=services)
%end