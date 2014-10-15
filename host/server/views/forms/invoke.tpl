<form method="POST" action="/packages/{{package}}/{{service}}/invoke">
    <p>Invoke <b></b>{{package}}/{{service}}</p>

    <table>
        % for param in params:
        <tr>
            <td>{{param}}</td>
            <td><input name="{{param}}"/></td>
        </tr>
        % end
    </table>

    <input type="submit" value="Run"/>
</form>