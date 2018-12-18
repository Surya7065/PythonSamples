import traceback
from string import Template

m = 'a|b|1|q|m|a'.split('|')
n = 'a|b|1.0|q|m|a'.split('|')

tolerances = '1:0.0, 3:0.0'.split(',')

tol_dict = dict()

for t in tolerances:
    t = t.strip().split(':')
    tol_dict[int(t[0])] = float(t[1])

html_list = []

html_str = Template('''<!doctype html>
<html lang="en">
<head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
    <title>Hello, world!</title>
</head>
<body style="margin:10px">
    
    <div class="panel-group">
        $results
    </div>
</body>
</html>
''')

results = []

for j in range(5):
    diffs = []

    for idx, val in enumerate(m):

        if idx > len(n) - 1:
            break

        if idx + 1 in tol_dict:
            try:
                val = float(val)
                temp = float(n[idx])
                if (val - temp) == tol_dict[idx + 1]:
                    pass
                else:
                    diffs.append(str(idx + 1) + ',' + str(val) + ',' + str(n[idx]))
                continue
            except:
                pass
                # traceback.print_exc()

        if val == n[idx]:
            # print idx, 'Equal'
            pass
        else:
            diffs.append(str(idx + 1) + ',' + str(val) + ',' + str(n[idx]))

    extra_lines_m = None
    extra_lines_n = None
    if len(m) > len(n):
        extra_lines_m = m[len(n):]
    elif len(m) < len(n):
        extra_lines_n = n[len(m):]

    print '\n'.join(diffs)
    print '=' * 5
    print extra_lines_m
    print '=' * 5
    print extra_lines_n

    print(len(diffs))
    if len(diffs) == 0:
        tr_lst = None
    else:
        tr_lst = []

        thead = '<table class="table table-bordered table-hover">\n' \
                '<thead>\n' \
                '<tr>\n' \
                '<th scope="col">Idx</th>\n' \
                '<th scope="col">Column Name</th>\n' \
                '<th scope="col">XML Value</th>\n' \
                '<th scope="col">DB Value</th>\n' \
                '</tr>\n' \
                '</thead>\n'
        tr_tmp = Template('\n<tbody>\n<tr>\n<td>$idx</td>\n<td>Dummy</td>\n<td>$m</td>\n<td>$n</td>\n</tr>')
        tr_lst.append(thead)

        for diff in diffs:
            diff = diff.split(',')
            tr_lst.append(tr_tmp.substitute(idx=diff[0], m=diff[1], n=diff[2]))

        tr_lst.append('\n</tbody>\n</table>')
    # print html_str.substitute(table='\n'.join(tr_lst) if tr_lst else None)

    html_extras = ''
    if extra_lines_m:
        html_extras = '<h6>Extra Values found in XML Output</h6>\n' + '<p>' + ','.join(extra_lines_m) + '</p>\n'
    if extra_lines_n:
        html_extras += '<h6>Extra Values found in DB Output</h6>\n' + '<p>' + ','.join(extra_lines_n) + '</p>\n'

    status = len(diffs)==0 and html_extras==''

    if status:
        status = '<h4 align="right"><span class="label label-success">Pass</span></h4>'
    else:
        status = '<h4 align="right"><span class="label label-danger">Fail</span></h4>'

    print status

    temp = Template('\n<div class="panel panel-default">\n<div class="panel-heading">\n<h4> Id: </h4></div> \n<div class="panel-body">\n$status<div class="col-sm-6">\n$table</div>\n<div class="col-sm-6">\n$extras</div></div></div>')

    results.append(temp.substitute(table='' if tr_lst is None else '\n'.join(tr_lst), status=status, extras=html_extras))



with open('ac.html', 'w') as f:
    f.write(html_str.substitute(results='\n'.join(results)))
