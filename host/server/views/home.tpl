% rebase('base.tpl', title='Home')

<h2>Register New Package</h2>
% include('forms/register.tpl')

% if packages:
<h2>Registered Packages</h2>
% include('packages/list.tpl', packages=packages)
%end