import os
def get_file_lines(filename):
    file = open(filename, "r")
    lines = []
    line = file.readline()
    while line:
        line = line.replace('\n', '')
        lines.append(line)
        line = file.readline()
    return lines

def get_protocol_num_to_str(protocol_filename):
    lines = get_file_lines(protocol_filename)
    protocol_to_str = {}
    for idx in range(1, len(lines)):
        line = lines[idx]
        split_content = line.split(",")
        if len(split_content) > 2:
            protocol_to_str[split_content[0]] = split_content[1]
    return protocol_to_str

def get_lookup_table(lookup_filename):
    lines = get_file_lines(lookup_filename)
    lookup_table_mapping = {}
    for row in range(1, len(lines)):
        split_content = lines[row].split(",")
        if len(split_content) < 3:
            continue
        dstport, protocol, tag = split_content
        dstport_key_val = lookup_table_mapping.get(dstport, {})
        dstport_key_val[protocol] = tag
        lookup_table_mapping[dstport] = dstport_key_val
    return lookup_table_mapping

def process_flow_logs(log_filename, lookup_table, protocol_to_str):
    lines = get_file_lines(log_filename)
    tag_frequency = {}
    port_combination_frequency = {}
    for line in lines:
        elems = line.split(" ")
        if len(elems) < 8:
            continue
        dstport = elems[6]
        protocol = elems[7]
        protocol_str = protocol_to_str[protocol].lower()
        tag = None
        if dstport in lookup_table and protocol_str in lookup_table[dstport]:
            tag = lookup_table[dstport][protocol_str]
        else:
            tag = "Untagged"
        tag_frequency[tag] = tag_frequency.get(tag, 0) + 1
        port_dict = port_combination_frequency.get(dstport, {})
        port_dict[protocol_str] = port_dict.get(protocol_str, 0) + 1
        port_combination_frequency[dstport] = port_dict
    return tag_frequency, port_combination_frequency

def add_to_file(output_filename, text):
    with open(output_filename, 'a') as file:
        file.write(text + "\n")

def write_tag_counts_to_output(tag_output_filename, tag_frequency):
    add_to_file(tag_output_filename, "Tag,Count")
    for key in tag_frequency:
        add_to_file(tag_output_filename, key + "," + str(tag_frequency[key]))

def write_port_combination_frequency(port_protocol_filename, port_combination_frequency):
    add_to_file(port_protocol_filename, "Port,Protocol,Count")
    for port in port_combination_frequency:
        for protocol in port_combination_frequency[port]:
            add_to_file(port_protocol_filename, port + "," + protocol + "," + str(port_combination_frequency[port][protocol]))

def delete_file(filename):
    if os.path.isfile(filename):
        os.remove(filename)

def main():
    delete_file("tag_counts.csv")
    delete_file("port_protocol_counts.csv")
    lookup_table = get_lookup_table("lookup.csv")
    protocol_num_to_str = get_protocol_num_to_str("protocol-numbers.csv")
    tag_frequency, port_combination_frequency = process_flow_logs("sample_flow_logs.txt", lookup_table, protocol_num_to_str)
    write_tag_counts_to_output("tag_counts.csv", tag_frequency)
    write_port_combination_frequency("port_protocol_counts.csv", port_combination_frequency)

if __name__ == "__main__":
    main()