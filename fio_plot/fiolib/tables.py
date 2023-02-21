import matplotlib.font_manager as font_manager


def get_widest_col(data):

    sizes = []
    for x in data:
        s = str(x)
        length = len(s)
        sizes.append(length)
    return sizes


def get_max_width(dataset, cols):
    matrix = []
    returndata = []
    for item in dataset:
        matrix.append(get_widest_col(item))

    col = 0
    while col < cols:
        column = 3
        for item in matrix:
            if item[col] > column:
                column = item[col]
        returndata.append(column)
        col += 1
    return returndata


def calculate_colwidths(settings, cols, matrix):

    collist = []

    for item in matrix:
        value = item * settings["tablecolumn_spacing"]
        collist.append(value)

    return collist


def get_font(settings):
    font = font_manager.FontProperties(size=settings["table_fontsize"])
    return font


def format_hostname_labels(settings, data):
    labels = []
    counter = 1
    hostcounter = 0 
    divide = int(len(data["hostname_series"]) / len(data["x_axis"])) # that int convert should work
    for host in data["hostname_series"]:
        hostcounter += 1
        attr = data["x_axis"][counter-1]
        labels.append(f"{host}\n{settings['graphtype'][-2:]} {attr}")
        if hostcounter % divide == 0:
            counter += 1
    return labels


def create_generic_table(settings, table_vals, ax2, rowlabels, location, fontsize):
    cols = len(table_vals[0])
    matrix = get_max_width(table_vals, cols)
    #matrix = [ x / 4 for x in matrix ]
    #print(matrix)
    colwidths = calculate_colwidths(settings, cols, matrix)
    #colwidths = [ x * 0.4 for x in colwidths]
    #print(colwidths)

    table = ax2.table(
        cellText=table_vals,
        loc=location,
        rowLabels=rowlabels,
        colLoc="center",
        colWidths=colwidths,
        cellLoc="center",
        rasterized=False,
    )
    table.auto_set_font_size(False) # Very Small
    table.scale(1, 1.2)

    if settings["table_lines"]:
        linewidth = 0.25
    else:
        linewidth = 0
    fontsettings = get_font(settings)
    fontsettings.set_size(fontsize)
    angle = 45
    if cols > 8:
        rotate = angle
    else:
        rotate = 0
    counter = 0 
    for key, cell in table.get_celld().items():
        cell.set_linewidth(linewidth)
        cell.set_text_props(fontproperties=fontsettings)
        if counter < (cols):
            cell.get_text().set_rotation(rotate)
            if rotate == angle:
                cell.set_height(0.8)
        if fontsize == 8 and max(matrix) > 5:
            cell.set_width(0.08)
        else:
            cell.set_width(0.04)
        counter += 1

def create_cpu_table(settings, data, ax2, fontsize):
    table_vals = [data["x_axis"], data["cpu"]["cpu_usr"], data["cpu"]["cpu_sys"]]

    rowlabels = ["CPU Usage", "cpu_usr %", "cpu_sys %"]
    location = "lower center"
    create_generic_table(settings, table_vals, ax2, rowlabels, location, fontsize)


def create_stddev_table(settings, data, ax2, fontsize):
    #print(data)
    if data["hostname_series"]:
        labels = format_hostname_labels(settings, data)
        table_vals = [labels, data["y1_axis"]["stddev"], data["y2_axis"]["stddev"]]
    else:
        table_vals = [data["x_axis"], data["y1_axis"]["stddev"], data["y2_axis"]["stddev"]]

    table_name = settings["label"]

    rowlabels = [table_name, "IOP/s \u03C3 %", "Latency \u03C3 %"]
    location = "lower right"
    create_generic_table(settings, table_vals, ax2, rowlabels, location, fontsize)


def convert_number_to_yes_no(data):
    newlist = []
    lookup = {1: "yes", 0: "no"}
    for item in data:
        newlist.append(lookup[item])
    return newlist


def create_steadystate_table(settings, data, ax2):
    # pprint.pprint(data)
    if data["ss_attained"]:
        data["ss_attained"] = convert_number_to_yes_no(data["ss_attained"])
        table_vals = [
            data["x_axis"],
            data["ss_data_bw_mean"]["data"],
            data["ss_data_iops_mean"]["data"],
            data["ss_attained"],
        ]

        rowlabels = [
            "Steady state",
            f"BW mean {data['ss_data_bw_mean']['format']}",
            f"{data['ss_data_iops_mean']['format']}  mean",
            f"{data['ss_settings'][0]} attained",
        ]
        location = "lower center"
        create_generic_table(settings, table_vals, ax2, rowlabels, location)
    else:
        print(
            "\n No steadystate data was found, so the steadystate table cannot be displayed.\n"
        )
