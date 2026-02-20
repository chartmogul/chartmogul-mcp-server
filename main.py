from chartmogul_mcp import mcp_server


def main():
    cm_mcp = mcp_server.ChartMogulMcp()
    cm_mcp.run()


if __name__ == "__main__":
    main()