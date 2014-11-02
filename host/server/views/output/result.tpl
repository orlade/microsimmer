% rebase('base.tpl', title='%s/%s Results' % (package, service))

<p>Invoked <a href="/packages/{{package}}">{{package}}</a>/<a
        href="/packages/{{package}}/{{service}}">{{service}}</a> with:</p>

<table>
    % for param, value in params.items():
    <tr>
        <td>{{param}}</td>
        <td>{{value}}</td>
    </tr>
    % end
</table>

<h2>Results</h2>

<pre>{{result}}</pre>
