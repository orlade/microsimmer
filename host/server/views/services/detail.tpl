% rebase('base.tpl', title='%s/%s Detail' % (package, service))

<h2>{{service}}</h2>

% include('forms/invoke.tpl', package=package, service=service, params=params)
